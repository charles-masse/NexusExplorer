
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

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
