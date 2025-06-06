
import os

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from singletons import settings, LocalizedStrings, loadManager
from actions.links import linkGameObject

from windows import mapViewer

import trimesh

from pprint import pprint # DEBUG

WINDOW_WIDTH = 400

class ContentLabel(QLabel):

    def __init__(self, text, name='ContentLabel'):
        super().__init__()
        # Create hyperlinks
        if '$' in text:
            text = linkGameObject(text)

        if name.startswith('localizedTextIdMoreInfoSay0') or name in ['localizedTextIdAcceptResponse', 'localizedTextIdCompleteResponse']:
            text = f'> <b>{text}</b>'

        self.setText(f'<div>{text.replace('\\n', '<br>')}</div>')
        self.setObjectName(name)
        self.setWordWrap(True)
        # Handle links
        self.setOpenExternalLinks(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.linkActivated.connect(self.popup)

        self.setFixedHeight(self.sizeHint().height())

    def popup(self, link):

        try:
            modelId = eval(link)['creature2ModelInfoId']
            modelPath = loadManager['Creature2ModelInfo'][modelId]['assetPath'].replace('.m3', '')
            modelName = modelPath.split('\\')[-1]

            scene = trimesh.load(f'{os.path.abspath(os.curdir)}/{settings['gameFiles']}/{modelPath}/{modelName}.gltf'.replace('\\', '/'))
            scene.show()

        except:
            pass

class Window(QWidget):

    def __init__(self, data, mapView):
        super().__init__()

        self.mapView = mapView

        pprint(data) # DEBUG
        # general title vs challenge title
        title = LocalizedStrings[data.get('localizedTextIdTitle')] or LocalizedStrings[data.get('localizedTextIdName')]

        self.setWindowTitle(title)
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.move(screen.x(), screen.y())

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(3)
        # Datacubes
        datacubeList = []
        
        for i in range(6):
            text = LocalizedStrings[data.get(f'localizedTextIdText0{i}', '0')]

            if text:
                datacubeList.append(text)

        if datacubeList:
            self.layout.addWidget(ContentLabel('\n'.join(datacubeList), 'localizedTextIdFull'))
        # Quests
        for string in [
                        'localizedTextIdText',
                        'localizedTextIdGiverTextUnknown',
                        *[s for i in range(5) for s in (f'localizedTextIdMoreInfoSay0{i}', f'localizedTextIdMoreInfoText0{i}')],
                        'localizedTextIdAcceptResponse',
                        'localizedTextIdGiverSayAccepted'
                       ]:
            self.createLabel(data.get(string), string)

        for i in reversed(range(6)):

            objectiveString = '' if i == 0 else i
            objective = data.get(f'objective0{objectiveString}')

            if objective:
                objectiveData = loadManager['QuestObjective'].get(objective)

                if objectiveData:
                    pprint(objectiveData)
                    self.createLabel(objectiveData['localizedTextIdFull'], 'QuestObjective')

                    for locId in range(4):

                        pos = loadManager['WorldLocation2'].get(objectiveData[f'worldLocationsIdIndicator0{locId}'])

                        if pos:
                            self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

                    self.addQuestDirections(objectiveData['questDirectionId'], i + 1)

        for string in [
                       'localizedTextIdReceiverTextAchieved',
                       'localizedTextIdCompleteResponse',
                       'localizedTextIdReceiverSayCompleted',
                       'localizedTextIdCompletedSummary'
                      ]:
            self.createLabel(data.get(string), string)
        # Event
        for objectiveId, objective in enumerate(data.get('PublicEventObjective', [])):

            objectiveData = loadManager['PublicEventObjective'].get(objective)
            
            if objectiveData:
                pprint(objectiveData)
                self.createLabel(objectiveData['localizedTextId'], 'PublicEventObjective')

                pos = loadManager['WorldLocation2'].get(objectiveData['worldLocation2Id'])
                if pos:
                    self.mapView.drawObjective(pos['position0'], pos['position2'], objectiveId + 1)

                self.addQuestDirections(objectiveData['questDirectionId'], objectiveId + 1)

        self.createLabel(data.get('localizedTextIdEnd'), 'localizedTextIdEnd')
        # Challenge
        self.createLabel(data.get('localizedTextIdProgress'), 'localizedTextIdProgress')
        # Path
        pathId = data.get('pathTypeEnum')
        if pathId:

            for string in ['localizedTextIdUnlock', 'localizedTextIdSoldierOrders']:
                self.createLabel(data.get(string), string)

            if data['pathMissionTypeEnum'] == '0': # Soldier-Security 'PathSoldierEventWave' ??? Wave info probably server side
                pass

            if data['pathMissionTypeEnum'] == '4': # Soldier-Assassinate
                assassination = loadManager['PathSoldierAssassinate'][data['objectId']]
                self.layout.addWidget(ContentLabel(f"Assassinate {assassination['count']} $(creature={assassination['creature2Id']})", 'PathObjective'))

            if data['pathMissionTypeEnum'] == '5': # Soldier-Demolition
                demolition = loadManager['PathSoldierActivate'][data['objectId']]
                pprint(demolition)
                self.layout.addWidget(ContentLabel(f"Destroy {demolition['count']} $(creature={demolition['creature2Id']})", 'PathObjective'))

            if data['pathMissionTypeEnum'] == '6': # Soldier-Rescue Op
                rescue = loadManager['PathSoldierActivate'][data['objectId']]
                self.layout.addWidget(ContentLabel(f"Rescue {rescue['count']} $(creature={rescue['creature2Id']})", 'PathObjective'))

            if data['pathMissionTypeEnum'] == '7': # Soldier-SWAT
                swat = loadManager['PathSoldierSWAT'][data['objectId']]
                
                group = loadManager['TargetGroup'].get(swat['targetGroupId'])
                
                if group:
                    groupName = LocalizedStrings[group['localizedTextIdDisplayString']]
                
                if not groupName:

                    creatures = []

                    for i in range(7):
                        creatureId = group[f'data{i}']

                        if creatureId != '0':
                            creatures.append(f"$(creature={creatureId})")

                    groupName = ', '.join(list(set(creatures)))

                else:

                    groupName = f'<i>{groupName}</i>'
                    
                self.layout.addWidget(ContentLabel(f"Kill {swat['count']} {groupName} with $(vitem={swat['virtualItemIdDisplay']})", 'PathObjective'))

            if data['pathMissionTypeEnum'] == '19': # Settler-Expansion
                hub = loadManager['PathSettlerHub'][data['objectId']] # Link ressource items?

            if data['pathMissionTypeEnum'] == '21': # Settler-Project
                infrastructure =  loadManager['PathSettlerInfrastructure'][data['objectId']] # Link hubs?

                self.createLabel(infrastructure.get('localizedTextIdObjective'), 'PathObjective')

            if data['pathMissionTypeEnum'] == '25': # Settler-Civil service
                mayor = loadManager['PathSettlerMayor'][data['objectId']] # Add locations of objectives to map

                for i in range(8):
                    self.createLabel(mayor.get(f'localizedTextId0{i}'), 'QuestObjective')

                    pos = loadManager['WorldLocation2'].get(mayor[f'worldLocation2Id0{i}'])
                    if pos:
                        self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

                    self.addQuestDirections(mayor.get(f'questDirectionId0{i}'), i + 1)

            if data['pathMissionTypeEnum'] == '26': # Settler-Public safety
                sheriff = loadManager['PathSettlerSheriff'][data['objectId']]

                for i in range(8):
                    descriptionId = LocalizedStrings[sheriff.get(f'localizedTextIdDescription0{i}')]
                    if descriptionId:
                        self.layout.addWidget(ContentLabel(f"{descriptionId}\\n$(quest={sheriff.get(f'quest2IdSheriff0{i}', '0')})", 'PathObjective'))

            if data['pathMissionTypeEnum'] == '27': # Settler-Cache
                pass # ???

            if data['pathMissionTypeEnum'] in ['2', '14']: # Scientist-Biology/Botany/Analysis/Diagnostic/Chemistry/Archeology
                pass # ???

            if data['pathMissionTypeEnum'] == '20': # Scientist-Field Study
                study = loadManager['PathScientistFieldStudy'][data['objectId']]

                for i in range(8):
                    self.createLabel(study[f'localizedTextIdChecklist0{i}'], 'QuestObjective')

                    pos = loadManager['WorldLocation2'].get(study[f'worldLocation2IdIndicator0{i}'])
                    
                    if pos:
                        self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

            if data['pathMissionTypeEnum'] == '23': # Scientist-Specimen
                specimen = loadManager['PathScientistSpecimenSurvey'][data['objectId']]

                for i in range(10):
                    self.createLabel(specimen[f'localizedTextIdObjective0{i}'], 'QuestObjective')

                    pos = loadManager['WorldLocation2'].get(specimen[f'worldLocation2Id0{i}'])
                    
                    if pos:
                        self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

                    self.addQuestDirections(specimen[f'questDirectionId0{i}'], i + 1)
                
            if data['pathMissionTypeEnum'] == '24': # Scientist-Datacube
                pass # It's just reading all the datacubes in a zone

            if data['pathMissionTypeEnum'] == '3': # Explorer-Stalking What is this???
                pass

            if data['pathMissionTypeEnum'] == '12': # Explorer-Exploration
                doorEntrance = loadManager['PathExplorerDoorEntrance'].get(data['objectId'])
                # There's also Door with group activate and kill
                if doorEntrance:
                    self.layout.addWidget(ContentLabel(f"<b>Entrance:</b> $(creature={doorEntrance['creature2IdSurface']})", 'PathObjective'))
                    self.layout.addWidget(ContentLabel(f"<b>Inside:</b> $(creature={doorEntrance['creature2IdMicro']})", 'PathObjective'))
                    
                    # 'worldLocation2IdSurfaceRevealed'  Not accurate--probably minimap position

            if data['pathMissionTypeEnum'] in ['13', '18']: # Explorer-Scavenger hunt
                hunt = loadManager['PathExplorerScavengerHunt'].get(data['objectId'])

                if hunt:
                    for i in range(7):
                        clue = loadManager['PathExplorerScavengerClue'].get(hunt[f'pathExplorerScavengerClueId0{i}'])

                        if clue:
                            clueString = LocalizedStrings[clue['localizedTextIdClue']]

                            creature = loadManager['Creature2'].get(clue['creature2Id'])

                            if creature:
                                clueString += f'\\n$(creature={clue['creature2Id']})'

                            else:
                                test = loadManager['TargetGroup'].get(clue['targetGroupId']) # REWORK ME

                                if test:
                                    clueString += f'\\n{LocalizedStrings[test['localizedTextIdDisplayString']]}'

                            self.layout.addWidget(ContentLabel(clueString, 'QuestObjective'))

                            pos = loadManager['WorldLocation2'].get(clue['worldLocation2IdMiniMap'])
                            if pos:
                                self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)
                
            if data['pathMissionTypeEnum'] == '15': # Explorer-Vista, Surveillance

                node = loadManager['PathExplorerNode']

                for x in node.values():
                    if x['pathExplorerAreaId'] == data['objectId']:

                        pos = loadManager['WorldLocation2'].get(x['worldLocation2Id'])
                        if pos:
                            self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

                        self.addQuestDirections(x['questDirectionId'], 1)

            if data['pathMissionTypeEnum'] == '16': # Explorer-Cartography--explore whole map? 'PathExplorerPowerMap'
                pass
                
            if data['pathMissionTypeEnum'] == '17': # Explorer-Operation
                operation = loadManager['PathExplorerActivate'][data['objectId']]

                self.layout.addWidget(ContentLabel(f"Investigate {operation['count']} $(creature={operation['creature2Id']})", 'PathObjective'))

        self.createLabel(data.get('localizedTextIdCommunicator'), 'localizedTextIdCommunicator')
        # Quest directions
        # PathMission, Quest, Challenge
        test = data.get('questDirectionId') or data.get('questDirectionIdCompletion') or data.get('questDirectionIdActive')

        if test:
            self.addQuestDirections(test, 1)

        self.setFixedWidth(WINDOW_WIDTH)
        # Add floating icons
        view = QGraphicsView(self)
        view.setStyleSheet("background: transparent; border: 0;")
        view.setFixedSize(WINDOW_WIDTH, self.sizeHint().height())
        view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, view.width(), view.height())
        view.setScene(scene)

        heightOffset = 0
        objId = 1

        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()

            if widget.objectName() in ['QuestObjective', 'PublicEventObjective']:
                test = mapViewer.ObjectiveIcon(objId)
                test.setPos(1, heightOffset)
                scene.addItem(test)
                objId += 1 

            heightOffset += widget.sizeHint().height() + 3
            
    def createLabel(self, stringId, name):
        """
        Create a label if it can find a localized text
        """
        localizedText = LocalizedStrings[stringId]

        if localizedText:
            self.layout.addWidget(ContentLabel(localizedText, name))

    def closeEvent(self, event):

        self.mapView.focusOn()

        event.accept()

    def addQuestDirections(self, directionId, number):

        questDirection = loadManager['QuestDirection'].get(directionId)

        if questDirection:
            for i in range(16):
                entry = loadManager['QuestDirectionEntry'].get(questDirection[f'questDirectionEntryId{str(i).zfill(2)}'])

                if entry:
                    pos = loadManager['WorldLocation2'].get(entry['worldLocation2Id'])

                    if pos:
                        self.mapView.drawObjective(pos['position0'], pos['position2'], number)
