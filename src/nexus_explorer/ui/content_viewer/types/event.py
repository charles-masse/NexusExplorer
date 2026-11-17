
from typing import TYPE_CHECKING

from .utilities import get_mission_context

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_event(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)
    #Objectives
    for objective_id, objective in enumerate(content.get('PublicEventObjective', [])):
        window.add_label(objective['localizedTextId'], 'LabelObjective')

        pos = loading_manager['WorldLocation2'].get(objective['worldLocation2Id'])
        if pos:
            window.add_map_location(pos, str(objective_id + 1))

    window.add_label(content.get('localizedTextIdEnd'), 'LabelInfo')
