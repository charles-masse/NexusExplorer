
from typing import TYPE_CHECKING

from nexus_explorer.data.utilities import link_referenced
from nexus_explorer.ui.content_viewer.labels import ContentLabel

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_event(window: "ContentViewerWindow"):
    #TODO parent event
    content = window.content

    for objective in content.get('PublicEventObjective', []):

        objective_text = link_referenced(window.loading_manager, objective['localizedTextId'])

        window.right_layout.addWidget(ContentLabel(objective_text, 'PublicEventObjective'))

    #         pos = loadManager['WorldLocation2'].get(objectiveData['worldLocation2Id'])
    #         if pos:
    #             self.mapView.drawObjective(pos['position0'], pos['position2'], objective_id + 1)

    #         self.addQuestDirections(objectiveData['questDirectionId'], objective_id + 1)

    text_end = content.get('localizedTextIdEnd')
    if text_end:
        window.right_layout.addWidget(ContentLabel(text_end, 'localizedTextIdEnd'))
