
import os
from typing import TYPE_CHECKING

from nexus_explorer.data.utilities import link_data  #replace_data

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
    #Objectives for events
    link_data(loading_manager, 'PublicEvent', 'publicEventId', ['PublicEventObjective'])
    #Linking zone related data
    link_data(loading_manager, 'WorldZone', 'worldzoneid', ['Datacube', 'MapZone'])
    #Location content
    link_data(loading_manager, 'WorldLocation2', 'worldlocation', [
        'Datacube',
        'PublicEvent',
        'Quest2',
        'QuestHub',
        'PathMission'
    ])
    #Only get the indicator for the challenge
    link_data(loading_manager, 'WorldLocation2', 'worldLocation2Idindicator', ['Challenge'])
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
        #Cleaning empty locations and revealing zones
        new_locations = []
        
        for location in world_data.locations:
            #Only use locations with content
            if any(location.get(key) for key in [
                'Challenge',
                'Datacube',
                'PublicEvent',
                'Quest2',
                'QuestHub',
                'PathMission'
            ]):
            
                world_zone = loading_manager['WorldZone'].get(location['worldZoneId'])
                if world_zone:
                    #Add zone to the location for naming purpose
                    if world_zone not in location.get('WorldZone', []):
                        location.setdefault('WorldZone', []).append(world_zone)
                    
                    map_zones = world_zone.get('MapZone')
                    if map_zones:
                        world_zone.setdefault('WorldLocation2', []).append(location)
                        #Add it to the list
                        if world_zone not in world_data.zones:
                            world_data.zones.append(world_zone)
                        
                    else:
                        new_locations.append(location)

        world_data.locations = new_locations
        # #Join zones #TODO Double-check
        for map_zone in loading_manager['MapZoneWorldJoin'].values():

            map_zone_data = loading_manager['MapZone'].get(map_zone['mapZoneId'])
            if map_zone_data:
                
                world_zone_data = loading_manager['WorldZone'].get(map_zone_data['worldZoneId'])
                if world_data and world_zone_data and world_data.id == map_zone['worldId'] and world_zone_data not in world_data.zones:
                    world_data.zones.append(world_zone_data)

    return worlds
