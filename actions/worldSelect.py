
from singletons import loadManager

def linkDb(linkDb, fieldName, sourceDbs):
    """
    Link referenced data ids to the actual data held by another database.

    linkDb (Dict): The database that holds the reference ids and will be returned.
    fieldName (String): Name of the field that contains the reference ids (in linkDb).
    sourceDbs (List of Dict): A list of databases that contains the data referenced by the ids.
    """
    for db in sourceDbs:
        for itemId, item in db.items():
            for key in [k for k in item if fieldName.lower() in k.lower()]:

                linkedItem = linkDb.get(item[key])

                if linkedItem:
                    linkedItem.setdefault(db.name, {})[itemId] = item

    return linkDb

def prepWorlds():
    # _buildQuestObjectives()
    # _buildEventObjectives()
    _buildLocations()
    _buildWorlds()

# def _buildQuestObjectives():
#     """
#     Link objectives to their quest.
#     """
#     quests = loadManager['Quest2']
#     questObjectives = loadManager['QuestObjective']

#     for quest in quests.values():
#         for objectiveId in ['objective0', 'objective01', 'objective02', 'objective03', 'objective04', 'objective05']:
#             objective = questObjectives.get(quest[objectiveId])

#             if objective:
#                 objective['Quest2'] = quest['itemId']

# def _buildEventObjectives():
#     """
#     Link objectives to their event.
#     """
#     events = loadManager['PublicEvent']
#     eventObjectives = loadManager['PublicEventObjective']

#     for objective in eventObjectives.values():
#         event = events.get(objective['publicEventId'])

#         if event:
#             event.setdefault('PublicEventObjective', []).append(objective['itemId'])

def _buildLocations():
    """
    Link all contents to their location
    """
    locations = linkDb(loadManager['WorldLocation2'], 'worldlocation', [
                                                                        loadManager['WorldZone'],
                                                                        loadManager['Challenge'],
                                                                        loadManager['Datacube'],
                                                                        loadManager['PublicEvent'],
                                                                        # loadManager['PublicEventObjective'],
                                                                        loadManager['Quest2'],
                                                                        # loadManager['QuestObjective'],
                                                                        loadManager['QuestHub'],
                                                                        loadManager['PathMission']
                                                                       ]) # 'QuestDirectionEntry' ???

def _buildWorlds():
    """
    Link location to their world.
    """
    worlds = loadManager['World']
    locations = loadManager['WorldLocation2']

    for locationId, locationData in locations.items():

        world = worlds.get(locationData['worldId'])
        
        if world:
            world.setdefault('WorldLocation2', {})[locationId] = locationData

prepWorlds()
