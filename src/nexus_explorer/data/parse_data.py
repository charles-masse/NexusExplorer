
import os
import re

from . import DBDict, LoadingManager, LocationData, WorldData


def link_data(target:DBDict, field_name:str, source:list[DBDict]) -> DBDict:
    """Link data that referenced the target
    - target: The database referenced and that will be returned.
    - field_name: Name of the field that contains the reference ids (in targetDb).
    - source: A list of databases that contains a reference to the target.
    """
    for db in source:
        for item in db.values():
            for key in [k for k in item if field_name.lower() in k.lower()]:
                #Add item that referenced this data
                linked_item = target.get(item[key])
                if linked_item:
                    linked_item.setdefault(db.name, []).append(DBDict(db.name, item))

    return target

def replace_data(target:DBDict, field_name:str, source:DBDict) -> DBDict:

    for item in target.values():
        for key in [k for k in item if field_name.lower() in k.lower()]:
            replacement_item = source.get(item[key])

            if replacement_item:
                item[key] = replacement_item

    return target

def prep_worlds(loading_manager: LoadingManager):
    """Link content to their location"""
    #Linking objectives to their quest and event
    replace_data(loading_manager['Quest2'], 'objective0', loading_manager['QuestObjective'])
    link_data(loading_manager['PublicEvent'], 'publicEventId', [loading_manager['PublicEventObjective']])
    #Adding zone datacubes
    link_data(loading_manager['WorldZone'], 'worldZoneId', [loading_manager['Datacube']])
    #Link content to their location
    replace_data(loading_manager['WorldLocation2'], 'worldZoneId', loading_manager['WorldZone'])
    link_data(loading_manager['WorldLocation2'], 'worldlocation', [
        loading_manager['Challenge'],
        loading_manager['Datacube'],
        loading_manager['PublicEvent'],
        loading_manager['PublicEventObjective'],
        loading_manager['Quest2'],
        loading_manager['QuestObjective'],
        loading_manager['QuestHub'],
        loading_manager['PathMission']
    ]) #'QuestDirectionEntry' #???
    #Link locations to their world
    link_data(loading_manager['World'], 'worldId', [loading_manager['WorldLocation2']])

    for world in loading_manager['World'].values():
        world_data = WorldData(**world)
        #Can we find the map in the files
        world_data.isMap = world_data.map_name in os.listdir(f"{loading_manager.game_files}/Map/")
        #Location cleanup
        cleaned_locs = []

        for location in world_data.locations:
            loc = LocationData(**location)
            
            if any([
                loc.challenges,
                loc.datacubes,
                loc.events,
                loc.event_objectives,
                loc.quests,
                loc.quest_objectives,
                loc.hubs,
                loc.missions
            ]):
                cleaned_locs.append(loc)

        world_data.locations = cleaned_locs
        #Add world to list if world has a map and/or locations with content
        if world_data.isMap or world_data.locations:
            loading_manager.worlds.append(world_data)

DATABASES = {
    'creature' : 'Creature2',
    'vitem' : 'VirtualItem',
    'item' : 'Item2',
    'schematic' : 'TradeskillSchematic2',
    'quest' : 'Quest2'
}

def link_referenced(loading_manager: LoadingManager, text: str, hyperlink: bool = True) -> str:
    """Add hypertext to a string.""" #TODO plural vs singular item
    regex = re.finditer(r'(?:<text[^>]*?>)?\$\S*?\((\w+)=(\d+)\)|\$(\w+)=(\d+)(?:</text>)?', text)
    for match in regex:

        full_match = match.group(0)
        db_name = match.group(1) or match.group(3)
        db_id = match.group(2) or match.group(4)

        linked = loading_manager[DATABASES[db_name.lower()]].get(int(db_id))

        if linked:
            linked_text = linked.get('localizedTextIdName')

        if not linked or not linked_text:
            linked_text = f"{db_name} id:{db_id} not found"

        if hyperlink: #TODO CBB
            text = text.replace(full_match, f'<b><a style="color: rgb(125, 251, 182);" href="{linked}">[{linked_text}]</a></b>')
        else:
            text = text.replace(full_match, f'[{linked_text}]')

    return text
