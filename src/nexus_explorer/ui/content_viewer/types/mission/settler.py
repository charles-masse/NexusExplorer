
from typing import TYPE_CHECKING
from urllib.parse import quote

from ..utilities import add_mission_locations, get_mission_context

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def settler_expansion(window: "ContentViewerWindow"):
     #TODO items, spells in PathSettlerImprovement
    content, loading_manager = get_mission_context(window)

    hub = loading_manager['PathSettlerHub'].get(content['objectId'])
    if hub:
        #Ressource locations
        for x in range(3):
            for y in range(4):
                loc = loading_manager['WorldLocation2'].get(hub[f'worldLocation2IdMapResource0{x}Loc0{y}'])
                if loc:
                    window.add_map_location(loc, 'X')

    depots: list[list] = []

    for improvement in loading_manager['PathSettlerImprovementGroup'].values():

        if improvement['pathSettlerHubId'] == content['objectId'] and improvement['creature2IdDepot'] not in [depot[0] for depot in depots]:
            depots.append([improvement['creature2IdDepot'], improvement['worldLocation2IdDisplayPoint']])

    depot_nb = 1

    for depot in depots:

        creature = loading_manager['Creature2'].get(depot[0])
        if creature:

            window.add_label(creature.get('localizedTextIdName'), 'LabelObjective')

            loc = loading_manager['WorldLocation2'].get(depot[1])
            if loc:
                window.add_map_location(loc, str(depot_nb))

            depot_nb += 1

    if hub:
        window.add_label(hub.get('localizedTextIdRewardNotify'), 'LabelChallenge0')

def settler_project(window: "ContentViewerWindow"):
    #TODO models, spells
    content, loading_manager = get_mission_context(window)

    infrastructure =  loading_manager['PathSettlerInfrastructure'].get(content['objectId'])
    if infrastructure:
        window.add_label(infrastructure.get('localizedTextIdObjective'), 'LabelObjective')
        #Target location
        add_mission_locations(window, content, '1')

def settler_service(window: "ContentViewerWindow"):
    #TODO title reward
    content, loading_manager = get_mission_context(window)

    mayor = loading_manager['PathSettlerMayor'].get(content['objectId'])
    if mayor:        
        for i in range(8):
            #Text
            window.add_label(mayor[f'localizedTextId0{i}'], 'LabelObjective')
            #Location
            loc = loading_manager['WorldLocation2'].get(mayor[f'worldLocation2Id0{i}'])
            if loc:
                window.add_map_location(loc, str(i + 1))
            #Direction
            directions = loading_manager['QuestDirection'].get(mayor[f'questDirectionId0{i}'])
            if directions:
                for x in range(16):
                    entry_id = directions[f'questDirectionEntryId{str(x).zfill(2)}']
                    dir = loading_manager['QuestDirectionEntry'].get(entry_id)
                    if dir:
                        loc = loading_manager['WorldLocation2'].get(dir['worldLocation2Id'])
                        if loc:
                            window.add_map_location(loc, str(i + 1))

def settler_safety(window: "ContentViewerWindow"):
    #TODO title reward
    content, loading_manager = get_mission_context(window)

    sheriff = loading_manager['PathSettlerSheriff'].get(content['objectId'])
    if sheriff:
        for i in range(8):
            #Linked quest
            quest = loading_manager['Quest2'].get(sheriff[f'quest2IdSheriff0{i}'])
            if quest:
                window.add_label(f'<b><a style="color: rgb(125, 251, 182);" href="{quote(str(quest))}">{sheriff[f"localizedTextIdDescription0{i}"]}</a></b>', 'LabelObjective')

                loc = loading_manager['WorldLocation2'].get(quest['WorldLocation2IdReceiver'])
                if loc:
                    window.add_map_location(loc, str(i + 1))
                #Alt receivers
                for i in range(3):
                    pos = loading_manager['WorldLocation2'].get(quest[f'worldLocation2IdAltReceiver0{i}'])
                    if pos:
                        window.add_map_location(pos, i + 1)
    #Start location(s)
    add_mission_locations(window, content, '-1')

def settler_cache(window: "ContentViewerWindow"):
    #TODO ???
    content, loading_manager = get_mission_context(window)
    #Target location(s)
    add_mission_locations(window, content, '1')
