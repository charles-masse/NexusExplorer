
from pprint import pprint
from typing import TYPE_CHECKING

from nexus_explorer.data.utilities import link_referenced
from nexus_explorer.ui.content_viewer.labels import ContentLabel

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow
    
def display_quest(window: "ContentViewerWindow"):
    #TODO faction req
    content = window.content

    pprint(content)

    for string in [
        'localizedTextIdText',
        'localizedTextIdGiverTextUnknown',
        *[s for i in range(5) for s in [f'localizedTextIdMoreInfoSay0{i}', f'localizedTextIdMoreInfoText0{i}']],
        'localizedTextIdAcceptResponse',
        'localizedTextIdGiverSayAccepted'
    ]:
        text = content.get(string)
        if text:
            text = link_referenced(window.loading_manager, text)
            window.right_layout.addWidget(ContentLabel(text, string))

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

    for string in [
        'localizedTextIdReceiverTextAchieved',
        'localizedTextIdCompleteResponse',
        'localizedTextIdReceiverSayCompleted',
        'localizedTextIdCompletedSummary'
    ]:
        text = content.get(string)
        if text:
            text = link_referenced(window.loading_manager, text)
            window.right_layout.addWidget(ContentLabel(text, string))
