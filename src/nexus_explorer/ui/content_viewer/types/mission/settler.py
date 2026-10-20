
from typing import TYPE_CHECKING

from nexus_explorer.ui.content_viewer.labels import ContentLabel

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow


def settler_expansion(window: "ContentViewerWindow"):

    # hub = loadManager['PathSettlerHub'][data['objectId']] # Link ressource items?

    pass

def settler_project(window: "ContentViewerWindow"):

    content = window.content

    infrastructure =  window.loading_manager['PathSettlerInfrastructure'].get(content['objectId']) # Link hubs?
    if infrastructure:
        window.right_layout.addWidget(ContentLabel(infrastructure.get('localizedTextIdObjective'), 'PathObjective'))

def settler_service(window: "ContentViewerWindow"):

    # mayor = loadManager['PathSettlerMayor'][data['objectId']] # Add locations of objectives to map

    # for i in range(8):
    #     self.createLabel(mayor.get(f'0{i}'), 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(mayor[f'worldLocation2Id0{i}'])
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #     self.addQuestDirections(mayor.get(f'questDirectionId0{i}'), i + 1)

    pass

def settler_safety(window: "ContentViewerWindow"):

    content = window.content

    sheriff = window.loading_manager['PathSettlerSheriff'].get(content['objectId'])

    if sheriff:
        for i in range(8):
            
            description_id = sheriff.get(f'Description0{i}')
            if description_id:
                window.right_layout.addWidget(ContentLabel(f"{description_id}\\n$(quest={sheriff.get(f'quest2IdSheriff0{i}', '0')})", 'PathObjective'))
    
def settler_cache(window: "ContentViewerWindow"):
    pass
