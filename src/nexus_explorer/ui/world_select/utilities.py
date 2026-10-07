
import os
from typing import TYPE_CHECKING

from nexus_explorer.data.utilities import link_data, replace_data

if TYPE_CHECKING:
    from nexus_explorer.data import LoadingManager

class WorldData:

    def __init__(
            self,
            ID: int,
            assetPath: str,
            localizedTextIdName: str,
            WorldLocation2: list[dict] | None = None,
            **kwargs
        ) -> None:

        self.id = ID
        self.map = assetPath
        self.name = localizedTextIdName
        
        self.name_map = assetPath.split('\\')[-1]

        self.locations = WorldLocation2 or []
        self.zones: list[dict] = []

def prep_worlds(loading_manager: "LoadingManager"):

    worlds = []
    #Objectives for quests and events
    replace_data(loading_manager, 'Quest2', 'objective0', 'QuestObjective')
    link_data(loading_manager, 'PublicEvent', 'publicEventId', ['PublicEventObjective'])
    #Zone datacubes
    link_data(loading_manager, 'WorldZone', 'worldZoneId', ['Datacube'])
    #Link map zones to their zone
    link_data(loading_manager, 'WorldZone', 'worldZoneId', ['MapZone'])
    #Location content
    link_data(loading_manager, 'WorldLocation2', 'worldlocation', [
        'Challenge',
        'Datacube',
        'PublicEvent',
        'PublicEventObjective',
        'Quest2',
        'QuestObjective',
        'QuestHub',
        'PathMission'
    ])
    #Link locations to their world
    link_data(loading_manager, 'World', 'worldId', ['WorldLocation2'])
    #Create world list
    for world in loading_manager['World'].values():
        world_data = WorldData(**world)
        #Use the continent name if the world is a continent
        if not world_data.name:
            for continent in loading_manager['MapContinent'].values():
                if continent['assetPath'] == world_data.map:
                    world_data.name = continent['localizedTextIdName']
                    break
        #Can we find the map in the game files
        map_found = world_data.name_map in os.listdir(f"{loading_manager.game_files}/Map/")
        if not map_found:
            world_data.map = ''

        worlds.append(world_data)
        #Revealing zones
        new_locations = []
        #TODO cleanup
        for location in world_data.locations:

            world_zone = loading_manager['WorldZone'].get(location['worldZoneId'])

            if world_zone:
                map_zone = world_zone.get('MapZone')

            if world_zone and map_zone and map_zone[0]["mapZoneIdParent"]:
                #Add it to the list
                if world_zone not in world_data.zones:
                    world_data.zones.append(world_zone)
                #Link location to their zone
                if any(location.get(key) for key in [
                    'Challenge',
                    'Datacube',
                    'PublicEvent',
                    'PublicEventObjective',
                    'Quest2',
                    'QuestObjective',
                    'QuestHub',
                    'PathMission'
                ]):
                    world_zone.setdefault('WorldLocation2', []).append(location)
                
            else:
                new_locations.append(location)
                    
        world_data.locations = new_locations
        #Join zones #TODO FIX THIS
        for map_zone in loading_manager['MapZoneWorldJoin'].values():

            map_zone_data = loading_manager['MapZone'].get(map_zone['mapZoneId'])
            
            if map_zone_data:
                world_zone_data = loading_manager['WorldZone'].get(map_zone_data['worldZoneId'])

                if world_data and world_zone_data and world_data.id == map_zone['worldId'] and world_zone_data not in world_data.zones:
                    world_data.zones.append(world_zone_data)

    return worlds
