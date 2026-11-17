
from typing import TYPE_CHECKING

from ..utilities import add_mission_locations, get_mission_context, get_target_group

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def explorer_stalking(window: "ContentViewerWindow"):
    #Place flags on important spots : no locations, scanner acts up when close to loc #TODO investigate
    pass

def explorer_exploration(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    door_entrance = loading_manager['PathExplorerDoorEntrance'].get(content['objectId'])

    if not door_entrance:
        window.add_label("Go through the secret passageway.", 'LabelObjective')

    else:
        #Entrance
        micro_name = 'the secret passageway'

        door = loading_manager['PathExplorerDoor'].get(door_entrance['pathExplorerDoorId'])
        if door:
            zone = loading_manager['WorldZone'].get(door.get('worldZoneIdInsideMicro'))
            if zone:
                micro_name = zone.get('localizedTextIdName') or micro_name
        # TODO show the door model on the left side
        window.add_label(f"Go through the $(creature={door_entrance['creature2IdSurface']}) into {micro_name}.",'LabelObjective')
        #Inside
        if door:
            target_group_id_activate = door['targetGroupIdActivate']
            if target_group_id_activate:
                window.add_label(f"Activate {get_target_group(loading_manager, target_group_id_activate)}.", 'LabelObjective')

            target_group_id_kill = door['targetGroupIdKill']
            if target_group_id_kill:
                window.add_label(f"Kill {get_target_group(loading_manager, target_group_id_kill)}.", 'LabelObjective')
    #Map start location(s)
    add_mission_locations(window, content, '-1')
        
def explorer_scavenger(window: "ContentViewerWindow"):
    #TODO spell, models
    content, loading_manager = get_mission_context(window)

    hunt = loading_manager['PathExplorerScavengerHunt'].get(content['objectId'])
    if hunt:
        #start
        window.add_label(hunt['localizedTextIdStart'], 'LabelRespond', hunt['assetPathSprite'])
        #Clues
        for i in range(7):
            clue = loading_manager['PathExplorerScavengerClue'].get(hunt[f'pathExplorerScavengerClueId0{i}'])
            if clue:
                window.add_label(clue['localizedTextIdClue'], 'LabelObjective')
                #Clue objective
                loc = loading_manager['WorldLocation2'].get(clue['worldLocation2IdMiniMap'])
                if loc:
                    window.add_map_location(loc, str(i + 1))
        #Start location(s)
        add_mission_locations(window, content, '-1')
    #For hunts where you have to follow a NPC
    else:
        window.add_label('Follow.', 'LabelObjective')
        #Start location(s)
        add_mission_locations(window, content, '1')

def explorer_vista(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    vista = loading_manager['PathExplorerNode'].get(content['objectId'])
    if vista:

        loc = loading_manager['WorldLocation2'].get(vista['worldLocation2Id'])
        if loc:
            #Add objective with vista's name
            vista_name = loading_manager['WorldZone'].get(loc['worldZoneId'], {}).get('localizedTextIdName') or 'the vista'
            window.add_label(f"Survey {vista_name}.", 'LabelObjective')

            window.add_map_location(loc, '1')
        #Start location(s)
        add_mission_locations(window, content, '-1')

    else:
        window.add_label("Survey vista.", 'LabelObjective')
        add_mission_locations(window, content, '1')

def explorer_cartography(window: "ContentViewerWindow"):
    #explore whole map #TODO objectId == MapZone 
    pass

def explorer_operation(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    operation = loading_manager['PathExplorerActivate'].get(content['objectId'])
    if operation:
        #Specific creature
        if operation['creature2Id']:
            window.add_label(f"Investigate {operation['count']} $(creature={operation['creature2Id']}).", 'LabelObjective', operation['count'])
        #Group of creatures
        else:
            window.add_label(f"Investigate {operation['count']} $(target={operation['targetGroupId']}).", 'LabelObjective', operation['count'])
    #Target location
    add_mission_locations(window, content, '1')
