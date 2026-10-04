
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
        self.zones: dict[int | None, list[dict | None]] = {}

def prep_worlds(loading_manager: "LoadingManager"):

    worlds = []
    #Objectives for quests and events
    replace_data(loading_manager, 'Quest2', 'objective0', 'QuestObjective')
    link_data(loading_manager, 'PublicEvent', 'publicEventId', ['PublicEventObjective'])
    #Zone datacubes
    link_data(loading_manager, 'WorldZone', 'worldZoneId', ['Datacube'])
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
    #List of zone ids that have a map
    map_zone_ids = [map_zone['worldZoneId'] for map_zone in loading_manager['mapZone'].values()]
    #Create world list
    for world in loading_manager['World'].values():
        world_data = WorldData(**world)
        #Use the continent name if the world is a continent
        if not world_data.name:
            for continent in loading_manager['mapContinent'].values():
                if continent['assetPath'] == world_data.map:
                    world_data.name = continent['localizedTextIdName']
                    break
        #Can we find the map in the game files #TODO
        map_found = world_data.name_map in os.listdir(f"{loading_manager.game_files}/Map/")
        if not map_found:
            world_data.map = ''

        worlds.append(world_data)
        #Revealing zones
        new_locations = []

        for location in world_data.locations:
            #Check if the location has content
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
                #Sort in their map zone or as a regular location
                zone_id = location['worldZoneId']
                if zone_id and zone_id in map_zone_ids:
                    world_data.zones.setdefault(zone_id, []).append(location)
                else:
                    new_locations.append(location)

        world_data.locations = new_locations

    return worlds
