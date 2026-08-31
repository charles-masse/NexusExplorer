
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from ...data import link_referenced
from .mission_types import (
    explorer_cartography,
    explorer_exploration,
    explorer_operation,
    explorer_scavenger,
    explorer_stalking,
    explorer_vista,
    scientist_analysis,
    scientist_datacube,
    scientist_experimentation,
    scientist_speciment,
    scientist_study,
    settler_cache,
    settler_expansion,
    settler_project,
    settler_safety,
    settler_service,
    soldier_assassinate,
    soldier_demolition,
    soldier_rescue,
    soldier_security,
    soldier_SWAT,
)

if TYPE_CHECKING:
    from . import ContentViewerWindow

class ContentLabel(QLabel):

    def __init__(self, text: str, name: str):
        super().__init__()
        #Class name for stylesheet
        self.setObjectName(name)
        #Create hyperlinks
        # if '$' in text:
        #     text = link_referenced(text)
        #User input text
        if any(name.startswith(string) for string in ['localizedTextIdMoreInfoSay0', 'localizedTextIdAcceptResponse', 'localizedTextIdCompleteResponse']):
            text = f'> <b>{text}</b>'

        self.setText(f'<div>{text.replace('\\n', '<br>')}</div>')

        self.setWordWrap(True)
        #Handle links
        self.setOpenExternalLinks(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.linkActivated.connect(self.popup)

        self.setFixedHeight(self.sizeHint().height())

    def popup(self, link):
        return link

    #     try:
    #         modelId = eval(link)['creature2ModelInfoId']
    #         modelPath = loadManager['Creature2ModelInfo'][modelId]['assetPath'].replace('.m3', '')
    #         modelName = modelPath.split('\\')[-1]

    #         scene = trimesh.load(f'{os.path.abspath(os.curdir)}/{settings['gameFiles']}/{modelPath}/{modelName}.gltf'.replace('\\', '/'))
    #         scene.show()

    #     except:
    #         pass

def display_datacube(window: "ContentViewerWindow"):
    #TODO Play sound
    content = window.content

    datacube_text = []

    image = content.get('assetPathImage')

    if image:

        image_file = image.replace('Icon_ItemTBF_', '')

        label = QLabel()
        pixmap = QPixmap(f'{window.loading_manager.game_files}/UI/Icon/Item/TBF/{image_file}/{image_file}.png')
        label.setPixmap(pixmap)
        window.main_layout.addWidget(label)

    for datacube_string_id in range(6):

        datacub_string = content.get(f'localizedTextIdText0{datacube_string_id}')

        if datacub_string:
            datacube_text.append(datacub_string)

    window.main_layout.addWidget(ContentLabel('\n'.join(datacube_text), 'QuestObjective'))

def display_quest(window: "ContentViewerWindow"):

    if window.content.name ==  'Quest2':

        for text_name in [
            'localizedTextIdText',
            'localizedTextIdGiverTextUnknown',
            *[s for i in range(5) for s in [f'localizedTextIdMoreInfoSay0{i}', f'localizedTextIdMoreInfoText0{i}']],
            'localizedTextIdAcceptResponse',
            'localizedTextIdGiverSayAccepted'
        ]:
            window.add_label(text_name)

    else:
        print('THIS IS AN OBJECTIVE')

#     for i in reversed(range(6)):

#         objectiveString = '' if i == 0 else i
#         objective = data.get(f'objective0{objectiveString}')

#         if objective:
#             objectiveData = loadManager['QuestObjective'].get(objective)

#             if objectiveData:
#                 pprint(objectiveData)
#                 self.createLabel(objectiveData['localizedTextIdFull'], 'QuestObjective')

#                 for locId in range(4):

#                     pos = loadManager['WorldLocation2'].get(objectiveData[f'worldLocationsIdIndicator0{locId}'])

#                     if pos:
#                         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

#                 self.addQuestDirections(objectiveData['questDirectionId'], i + 1)

#     for string in [
#                    'localizedTextIdReceiverTextAchieved',
#                    'localizedTextIdCompleteResponse',
#                    'localizedTextIdReceiverSayCompleted',
#                    'localizedTextIdCompletedSummary'
#                   ]:
#         self.createLabel(data.get(string), string)

def display_event(window: "ContentViewerWindow"):
    #TODO type?, parent
#     for objectiveId, objective in enumerate(data.get('PublicEventObjective', [])):

#         objectiveData = loadManager['PublicEventObjective'].get(objective)
        
#         if objectiveData:
#             pprint(objectiveData)
#             self.createLabel(objectiveData['localizedTextId'], 'PublicEventObjective')

#             pos = loadManager['WorldLocation2'].get(objectiveData['worldLocation2Id'])
#             if pos:
#                 self.mapView.drawObjective(pos['position0'], pos['position2'], objectiveId + 1)

#             self.addQuestDirections(objectiveData['questDirectionId'], objectiveId + 1)

#     self.createLabel(data.get('localizedTextIdEnd'), 'localizedTextIdEnd')

    window.add_label('localizedTextIdEnd')

def display_challenge(window: "ContentViewerWindow"):
    #TODO type?, target, flag?, quest directions, items
    #The location string seems to be the same as the actual location name in most cases--double-check
    window.add_label('localizedTextIdProgress')

def display_mission(window: "ContentViewerWindow"):

    window.add_label('localizedTextIdUnlock')
    window.add_label('localizedTextIdSoldierOrders')

    mission_id = window.content['pathMissionTypeEnum']
    
    if mission_id in [0]:
        soldier_security(window)

    elif mission_id in [2, 14]:
        scientist_analysis(window)

    elif mission_id in [3]:
        explorer_stalking(window)

    elif mission_id in [4]:
        soldier_assassinate(window)

    elif mission_id in [5]:
        soldier_demolition(window)

    elif mission_id in [6]:
        soldier_rescue(window)

    elif mission_id in [7]:
        soldier_SWAT(window)

    elif mission_id in [12]:
        explorer_exploration(window)

    elif mission_id in [13, 18]:
        explorer_scavenger(window)

    elif mission_id in [15]:
        explorer_vista(window)

    elif mission_id in [16]:
        explorer_cartography(window)

    elif mission_id in [17]:
        explorer_operation(window)

    elif mission_id in [19]:
        settler_expansion(window)

    elif mission_id in [20]:
        scientist_study(window)
        
    elif mission_id in [21]:
        settler_project(window)

    elif mission_id in [22]:
        scientist_experimentation(window)

    elif mission_id in [23]:
        scientist_speciment(window)

    elif mission_id in [24]:
        scientist_datacube(window)

    elif mission_id in [25]:
        settler_service(window)

    elif mission_id in [26]:
        settler_safety(window)

    elif mission_id in [27]:
        settler_cache(window)
    
    else:
        raise TypeError(f'Cannot parse this path mission id {mission_id}.')

    window.add_label('localizedTextIdCommunicator')
