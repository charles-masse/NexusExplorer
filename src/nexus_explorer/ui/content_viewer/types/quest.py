
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_quest(window: "ContentViewerWindow"):

    # if window.content.name ==  'Quest2':

    for text_name in [
        'localizedTextIdText',
        'localizedTextIdGiverTextUnknown',
        *[s for i in range(5) for s in [f'localizedTextIdMoreInfoSay0{i}', f'localizedTextIdMoreInfoText0{i}']],
        'localizedTextIdAcceptResponse',
        'localizedTextIdGiverSayAccepted'
    ]:
        window.add_label(text_name)

    # else:
    #     print('THIS IS AN OBJECTIVE')

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
