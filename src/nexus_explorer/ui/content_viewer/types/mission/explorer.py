
from typing import TYPE_CHECKING

from nexus_explorer.ui.content_viewer.labels import ContentLabel

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
        window.right_layout.addWidget(ContentLabel(f"<b>Entrance:</b> $(creature={doorEntrance['creature2IdSurface']})", 'PathObjective'))
        window.right_layout.addWidget(ContentLabel(f"<b>Inside:</b> $(creature={doorEntrance['creature2IdMicro']})", 'PathObjective'))
        # 'worldLocation2IdSurfaceRevealed' #TODO check

def explorer_scavenger(window: "ContentViewerWindow"):

    # hunt = loadManager['PathExplorerScavengerHunt'].get(data['objectId'])

    # if hunt:
    #     for i in range(7):
    #         clue = loadManager['PathExplorerScavengerClue'].get(hunt[f'pathExplorerScavengerClueId0{i}'])

    #         if clue:
    #             clueString = LocalizedStrings[clue['Clue']]

    #             creature = loadManager['Creature2'].get(clue['creature2Id'])

    #             if creature:
    #                 clueString += f'\\n$(creature={clue['creature2Id']})'

    #             else:
    #                 test = loadManager['TargetGroup'].get(clue['targetGroupId']) # REWORK ME

    #                 if test:
    #                     clueString += f'\\n{LocalizedStrings[test['DisplayString']]}'

    #             self.layout.addWidget(ContentLabel(clueString, 'QuestObjective'))

    #             pos = loadManager['WorldLocation2'].get(clue['worldLocation2IdMiniMap'])
    #             if pos:
    #                 self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)
    pass

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
    if operation:
        window.right_layout.addWidget(ContentLabel(f"Investigate {operation['count']} $(creature={operation['creature2Id']})", 'PathObjective'))
