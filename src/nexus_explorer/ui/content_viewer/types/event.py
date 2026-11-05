
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_event(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager
    #Objectives
    for objective_id, objective in enumerate(content.get('PublicEventObjective', [])):
        window.add_label(objective['localizedTextId'], 'LabelObjective')

        pos = loading_manager['WorldLocation2'].get(objective['worldLocation2Id'])
        if pos:
            window.add_map_location(pos, str(objective_id + 1))

    window.add_label(content.get('localizedTextIdEnd'), 'LabelInfo')
