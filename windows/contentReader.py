
import os

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from singletons import settings, LocalizedStrings, loadManager
from actions.links import linkGameObject

import trimesh

from pprint import pprint # DEBUG

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

    def __init__(self, data):
        super().__init__()

        pprint(data) # DEBUG
        # general title vs challenge title
        title = LocalizedStrings[data.get('localizedTextIdTitle')] or LocalizedStrings[data.get('localizedTextIdName')]

        self.setWindowTitle(title)

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

        for i in [''] + list(range(1, 6)):

            objectiveId = data.get(f'objective0{i}')

            if objectiveId:
                objective = loadManager['QuestObjective'].get(objectiveId)

                if objective:
                    self.createLabel(objective['localizedTextIdFull'], 'localizedTextIdFull')

        for string in [
                       'localizedTextIdReceiverTextAchieved',
                       'localizedTextIdCompleteResponse',
                       'localizedTextIdReceiverSayCompleted',
                       'localizedTextIdCompletedSummary'
                      ]:
            self.createLabel(data.get(string), string)
        # Event
        for objectiveId in data.get('PublicEventObjective', []):
            self.createLabel(loadManager['PublicEventObjective'].get(objectiveId)['localizedTextId'], 'PublicEventObjective')

        self.createLabel(data.get('localizedTextIdEnd'), 'localizedTextIdEnd')
        # Challenge
        self.createLabel(data.get('localizedTextIdProgress'), 'localizedTextIdProgress')
        # Path
        for string in ['localizedTextIdUnlock', 'localizedTextIdSoldierOrders']:
            self.createLabel(data.get(string), string)

        pathId = data.get('pathTypeEnum')

        if pathId == '0': # Soldier

            if data['pathMissionTypeEnum'] == '0': # Security
                eventWave = loadManager['PathSoldierEventWave'][data['objectId']] # ??? Wave info probably server side

            if data['pathMissionTypeEnum'] == '4': # Assassinate
                assassination = loadManager['PathSoldierAssassinate'][data['objectId']]
                self.layout.addWidget(ContentLabel(f"Assassinate {assassination['count']} $(creature={assassination['creature2Id']})", 'PathSoldierObjective'))

            if data['pathMissionTypeEnum'] == '5': # Demolition
                demolition = loadManager['PathSoldierActivate'][data['objectId']]
                self.layout.addWidget(ContentLabel(f"Destroy {demolition['count']} $(creature={demolition['creature2Id']})", 'PathSoldierObjective'))

            if data['pathMissionTypeEnum'] == '6': # Rescue Op
                rescue = loadManager['PathSoldierActivate'][data['objectId']]
                self.layout.addWidget(ContentLabel(f"Rescue {rescue['count']} $(creature={rescue['creature2Id']})", 'PathSoldierObjective'))

            if data['pathMissionTypeEnum'] == '7': # SWAT
                swat = loadManager['PathSoldierSWAT'][data['objectId']] # Where do I find group info?
                self.layout.addWidget(ContentLabel(f"Kill {swat['count']} $(creature={swat['targetGroupId']}) with $(vitem={swat['virtualItemIdDisplay']})", 'PathSoldierObjective'))

        if pathId == '1': # Settler

            if data['pathMissionTypeEnum'] == '19': # Expansion
                hub = loadManager['PathSettlerHub'][data['objectId']] # Link ressource items?

            if data['pathMissionTypeEnum'] == '21': # Project
                infrastructure =  loadManager['PathSettlerInfrastructure'][data['objectId']] # Link hubs?

                self.createLabel(infrastructure.get('localizedTextIdObjective'), 'PathSettlerObjective')

            if data['pathMissionTypeEnum'] == '25': # Civil service
                mayor = loadManager['PathSettlerMayor'][data['objectId']] # Add locations of objectives to map

                for i in range(8):
                    self.createLabel(mayor.get(f'localizedTextId0{i}'), 'PathSettlerObjective')

            if data['pathMissionTypeEnum'] == '26': # Public safety
                sheriff = loadManager['PathSettlerSheriff'][data['objectId']]

                for i in range(8):
                    descriptionId = LocalizedStrings[sheriff.get(f'localizedTextIdDescription0{i}')]
                    if descriptionId:
                        self.layout.addWidget(ContentLabel(f"{descriptionId}\\n$(quest={sheriff.get(f'quest2IdSheriff0{i}', '0')})", 'PathSettlerObjective'))

            if data['pathMissionTypeEnum'] == '27': # Cache
                pass

        if pathId == '2': # Scientist
            
            if data['pathMissionTypeEnum'] == '2': # Biology/Botany/Analysis/Diagnostic
                pass

            if data['pathMissionTypeEnum'] == '14': # Chemistry/Archeology
                pass

            if data['pathMissionTypeEnum'] == '20': # Field Study
                pass

            if data['pathMissionTypeEnum'] == '23': # Specimen
                pass

            if data['pathMissionTypeEnum'] == '24': # Datacube
                pass

        if pathId == '3': # Explorer
            
            if data['pathMissionTypeEnum'] == '3': # Claim
                pass

            if data['pathMissionTypeEnum'] == '12': # Exploration
                pass

            if data['pathMissionTypeEnum'] == '13': # Scavenger hunt
                pass

            if data['pathMissionTypeEnum'] == '15': # Surveillance
                pass

            if data['pathMissionTypeEnum'] == '16': # Cartography
                pass

            if data['pathMissionTypeEnum'] == '17': # Operation
                pass

            if data['pathMissionTypeEnum'] == '18': # Tracking
                pass

        self.createLabel(data.get('localizedTextIdCommunicator'), 'localizedTextIdCommunicator')

        self.setFixedWidth(400)

    def createLabel(self, stringId, name):

        localizedText = LocalizedStrings[stringId]

        if localizedText:
            self.layout.addWidget(ContentLabel(localizedText, name))
