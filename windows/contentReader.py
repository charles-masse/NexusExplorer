
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

        if name.startswith('localizedTextIdMoreInfoSay0'):
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
                        'localizedTextIdGiverSayAccepted',
                        'localizedTextIdReceiverTextAccepted'
                       ]:
            self.createLabel(data.get(string), string)

        for i in [''] + list(range(1, 6)):
            objectiveId = data.get(f'objective0{i}')

            if objectiveId:
                objective = loadManager['QuestObjective'].get(objectiveId)

                if objective:
                    self.createLabel(objective['localizedTextIdFull'], 'localizedTextIdFull')

        for string in [
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

        self.setFixedWidth(400)

        screen = QGuiApplication.primaryScreen().availableGeometry()
        screenCenter = screen.center()

        windowGeo = self.frameGeometry()
        windowGeo.moveCenter(screenCenter)

        self.move(windowGeo.topLeft())

    def createLabel(self, stringId, name):

        localizedText = LocalizedStrings[stringId]

        if localizedText:
            self.layout.addWidget(ContentLabel(localizedText, name))
