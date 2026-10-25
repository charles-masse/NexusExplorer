
from typing import TYPE_CHECKING

from nexus_explorer.data.utilities import link_referenced

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_event(window: "ContentViewerWindow"):
    #TODO parent event
    content = window.content

    for objective in content.get('PublicEventObjective', []):
        window.add_label(objective['localizedTextId'], 'LabelObjective')

    #         pos = loadManager['WorldLocation2'].get(objectiveData['worldLocation2Id'])
    #         if pos:
    #             self.mapView.drawObjective(pos['position0'], pos['position2'], objective_id + 1)

    #         self.addQuestDirections(objectiveData['questDirectionId'], objective_id + 1)

    text_end = content.get('localizedTextIdEnd')
    window.add_label(text_end, 'LabelInfo')
