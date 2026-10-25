
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def explorer_stalking(window: "ContentViewerWindow"):
    #What is this???
    pass

def explorer_exploration(window: "ContentViewerWindow"):

    content = window.content

    doorEntrance = window.loading_manager['PathExplorerDoorEntrance'].get(content['objectId'])
    #There's also Door with group activate and kill
    if doorEntrance:
        window.add_label(f"<b>Entrance:</b> $(creature={doorEntrance['creature2IdSurface']})", 'LabelObjective')
        window.add_label(f"<b>Inside:</b> $(creature={doorEntrance['creature2IdMicro']})", 'LabelObjective')
        # 'worldLocation2IdSurfaceRevealed' #TODO check

def explorer_scavenger(window: "ContentViewerWindow"):

    content = window.content

    clueString = []

    hunt = window.loading_manager['PathExplorerScavengerHunt'].get(content['objectId'])
    if hunt:
        for i in range(7):
            clue = window.loading_manager['PathExplorerScavengerClue'].get(hunt[f'pathExplorerScavengerClueId0{i}'])
            if clue:
                creature = window.loading_manager['Creature2'].get(clue['creature2Id'])
                if creature:
                    clueString += f'\\n$(creature={clue['creature2Id']})'

                else:
                    test = window.loading_manager['TargetGroup'].get(clue['targetGroupId']) # REWORK ME
                    if test:
                        clueString += f'\\n{test['localizedTextIdDisplayString']}'

                window.add_label(' '.join(clueString), 'LabelObjective')

    #             pos = loadManager['WorldLocation2'].get(clue['worldLocation2IdMiniMap'])
    #             if pos:
    #                 self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

def explorer_vista(window: "ContentViewerWindow"):

    # node = window.loading_manager['PathExplorerNode']

    # for x in node.values():
    #     if x['pathExplorerAreaId'] == data['objectId']:

    #         pos = loadManager['WorldLocation2'].get(x['worldLocation2Id'])
    #         if pos:
    #             self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #         self.addQuestDirections(x['questDirectionId'], 1)

    pass

def explorer_cartography(window: "ContentViewerWindow"):
    #explore whole map 'PathExplorerPowerMap'
    pass

def explorer_operation(window: "ContentViewerWindow"):

    content = window.content

    operation = window.loading_manager['PathExplorerActivate'].get(content['objectId'])
    window.add_label(f"Investigate {operation['count']} $(creature={operation['creature2Id']})", 'LabelObjective')
