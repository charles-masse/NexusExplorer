
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .mission_types import (
    explorer_cartography,
    explorer_exploration,
    explorer_operation,
    explorer_scavenger,
    explorer_stalking,
    explorer_vista,
    scientist_analysis,
    scientist_datacube,
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


class ContentLabel(QLabel):

    def __init__(self, text, name='ContentLabel'):
        super().__init__()
        # Create hyperlinks
        # if '$' in text:
        #     text = linkGameObject(text)

        if name.startswith('localizedTextIdMoreInfoSay0') or name in ['localizedTextIdAcceptResponse', 'localizedTextIdCompleteResponse']:
            text = f'> <b>{text}</b>'

        self.setText(f'<div>{text.replace('\\n', '<br>')}</div>')
        self.setObjectName(name)
        self.setWordWrap(True)
        # Handle links
        # self.setOpenExternalLinks(False)
        # self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        # self.linkActivated.connect(self.popup)

        self.setFixedHeight(self.sizeHint().height())

    # def popup(self, link):

    #     try:
    #         modelId = eval(link)['creature2ModelInfoId']
    #         modelPath = loadManager['Creature2ModelInfo'][modelId]['assetPath'].replace('.m3', '')
    #         modelName = modelPath.split('\\')[-1]

    #         scene = trimesh.load(f'{os.path.abspath(os.curdir)}/{settings['gameFiles']}/{modelPath}/{modelName}.gltf'.replace('\\', '/'))
    #         scene.show()

    #     except:
    #         pass

def display_datacube(content):
    #TODO Play sound
    datacube_text = []

    for datacube_string_id in range(6):

        datacub_string = content.get(f'text0{datacube_string_id}')

        if datacub_string:
            datacube_text.append(datacub_string)

    return [ContentLabel('\n'.join(datacube_text), 'localizedTextIdFull')]

def display_quest(content):

    widgets = []

    for text_name in [
        'text',
        'giverTextUnknown',
        *[s for i in range(5) for s in [f'moreInfoSay0{i}', f'moreInfoText0{i}']],
        'acceptResponse',
        'giverSayAccepted'
    ]:

        quest_text = content.get(text_name)

        if quest_text:
            widgets.append(ContentLabel(quest_text))

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

    return widgets

def display_event(loading_manager, content):
    #TODO type?, parent
    widgets = []
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

    loading_manager['en-US'].get(content.get(''))

    end_text = content.get('End')
    if end_text:
        widgets.append(ContentLabel(end_text))

    return widgets

def display_challenge(content):
    #TODO type?, target, flag?, quest directions, items
    #The location string seems to be the same as the actual location name in most cases--double-check
    widgets = []

    progress_text = content.get('progress')
    if progress_text:
        widgets.append(ContentLabel(progress_text))

    return widgets

def display_mission(content):

    widgets = []

    unlock_text = content.get('unlock')
    if unlock_text:
        widgets.append(ContentLabel(unlock_text))

    orders_text = content.get('soldierOrders')
    if orders_text:
        widgets.append(ContentLabel(orders_text))

    mission_id = content['pathTypeEnum']

    if mission_id in ['0']:
        widgets.extends(soldier_security(content))

    elif mission_id in ['2', '14']:
        widgets.extends(scientist_analysis(content))

    elif mission_id in ['3']:
        widgets.extends(explorer_stalking(content))

    elif mission_id in ['4']:
        widgets.extends(soldier_assassinate(content))

    elif mission_id in ['5']:
        widgets.extends(soldier_demolition(content))

    elif mission_id in ['6']:
        widgets.extends(soldier_rescue(content))

    elif mission_id in ['7']:
        widgets.extends(soldier_SWAT(content))

    elif mission_id in ['12']:
        widgets.extends(explorer_exploration(content))

    elif mission_id in ['13', '18']:
        widgets.extends(explorer_scavenger(content))

    elif mission_id in ['15']:
        widgets.extends(explorer_vista(content))

    elif mission_id in ['16']:
        widgets.extends(explorer_cartography(content))

    elif mission_id in ['17']:
        widgets.extends(explorer_operation(content))

    elif mission_id in ['19']:
        widgets.extends(settler_expansion(content))

    elif mission_id in ['20']:
        widgets.extends(scientist_study(content))
        
    elif mission_id in ['21']:
        widgets.extends(settler_project(content))

    elif mission_id in ['23']:
        widgets.extends(scientist_speciment(content))

    elif mission_id in ['24']:
        widgets.extends(scientist_datacube(content))

    elif mission_id in ['25']:
        widgets.extends(settler_service(content))

    elif mission_id in ['26']:
        widgets.extends(settler_safety(content))

    elif mission_id in ['27']:
        widgets.extends(settler_cache(content))
    
    else:
        raise TypeError(f'Cannot parse this path mission id {mission_id}.')

    communicator_text = content.get('communicator')
    if communicator_text:
        widgets.append(ContentLabel(communicator_text))

    return widgets
