
import os

from . import DBDict, WorldData


def linkDb(targetDb, fieldName, sourceDbs):
    """Link data that referenced the target

    targetDb (Dict): The database referenced and that will be returned.
    fieldName (String): Name of the field that contains the reference ids (in targetDb).
    sourceDbs (List of Dict): A list of databases that contains a reference to the target.
    """
    for db in sourceDbs:
        for item in db.values():
            for key in [k for k in item if fieldName.lower() in k.lower()]:
                #Add item that referenced this data
                linkedItem = targetDb.get(item[key])
                if linkedItem:
                    linkedItem.setdefault(db.name, []).append(DBDict(db.name, item))

    return targetDb

# def _buildQuestObjectives():
#     """Link objectives to their quest.
#     """
#     quests = loadManager['Quest2']
#     questObjectives = loadManager['QuestObjective']

#     for quest in quests.values():
#         for objectiveId in ['objective0', 'objective01', 'objective02', 'objective03', 'objective04', 'objective05']:
#             objective = questObjectives.get(quest[objectiveId])

#             if objective:
#                 objective['Quest2'] = quest['itemId']

# def _buildEventObjectives():
#     """Link objectives to their event.
#     """
#     events = loadManager['PublicEvent']
#     eventObjectives = loadManager['PublicEventObjective']

#     for objective in eventObjectives.values():
#         event = events.get(objective['publicEventId'])

#         if event:
#             event.setdefault('PublicEventObjective', []).append(objective['itemId'])

def prep_worlds(loading_manager):
    #Link content to their location
    linkDb(loading_manager['WorldLocation2'], 'worldlocation', [
        loading_manager['WorldZone'],
        loading_manager['Challenge'], #Link in world zone instead?
        loading_manager['Datacube'],
        loading_manager['PublicEvent'], #Link in world zone instead?
        loading_manager['Quest2'],
        loading_manager['QuestHub'],
        loading_manager['PathMission']
    ]) # 'QuestDirectionEntry' #???
    #Link locations to their world
    linkDb(loading_manager['World'], 'worldId', [loading_manager['WorldLocation2']])

    for world in loading_manager['World'].values():
        world_data = WorldData(**world)
        #Can we find the map in the files
        world_data.isMap = world_data.map_name in os.listdir(f"{loading_manager.game_files}/Map/")
        #Add world to list if world has a map and/or locations
        if world_data.isMap or len(world_data.locations):
            world_data.cleanup_locations()
            loading_manager.worlds.append(world_data)
