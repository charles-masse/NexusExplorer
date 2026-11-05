
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def settler_expansion(window: "ContentViewerWindow"):
     #TODO items, spells in PathSettlerImprovement
    content = window.content
    loading_manager = window.loading_manager

    hub = loading_manager['PathSettlerHub'].get(content['objectId'])
    if hub:
        #Ressource locations
        for x in range(3):
            for y in range(4):
                loc = loading_manager['WorldLocation2'].get(hub[f'worldLocation2IdMapResource0{x}Loc0{y}'])
                if loc:
                    window.add_map_location(loc, 'X')

    depots: list[int, str] = []

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
    content = window.content
    loading_manager = window.loading_manager

    infrastructure =  loading_manager['PathSettlerInfrastructure'].get(content['objectId'])
    if infrastructure:
        window.add_label(infrastructure.get('localizedTextIdObjective'), 'LabelObjective')
        #Target location
        for i in range(4):
            loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
            if loc:
                window.add_map_location(loc, '1')

def settler_service(window: "ContentViewerWindow"):
    #TODO title reward
    content = window.content
    loading_manager = window.loading_manager

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
    #TODO title reward, link to quest
    content = window.content
    loading_manager = window.loading_manager

    sheriff = loading_manager['PathSettlerSheriff'].get(content['objectId'])
    if sheriff:
        for i in range(8):
            window.add_label(sheriff.get(f'localizedTextIdDescription0{i}'), 'LabelObjective')
            #Linked quest
            quest = loading_manager['Quest2'].get(sheriff[f'quest2IdSheriff0{i}'])
            if quest:
                loc = loading_manager['WorldLocation2'].get(quest['WorldLocation2IdReceiver']) #TODO alt receivers
                if loc:
                    window.add_map_location(loc, str(i + 1))
    #Start location(s)
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '-1')

def settler_cache(window: "ContentViewerWindow"):
    #TODO ???
    content = window.content
    loading_manager = window.loading_manager
    #Target location(s)
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '1')
