
import os

from model import loadManager
from model.load_data import LocalizedStrings


class WorldData:

    def __init__(self, itemId, assetPath, chunkBounds00, chunkBounds01, chunkBounds02, chunkBounds03, localizedTextIdName, **kargs):

        self.id = itemId
        self.chunkBounds = [
                            chunkBounds00,
                            chunkBounds01,
                            chunkBounds02,
                            chunkBounds03,
                           ]
        
        self.name = LocalizedStrings[localizedTextIdName]

        self.map_name = assetPath.split('\\')[-1]
        self.map = self.retrieve_map()

        self.locations = []

        self._link_locations()

        # # _buildQuestObjectives()
        # _buildEventObjectives()
        # _buildLocations()
        # _buildWorlds()

    
    def _link_locations(self):
        """Link locations to their world.
        """
        locations = loadManager['WorldLocation2']

        for location in locations.values():
            if location['worldId'] == self.id:
                self.locations.append(1)

    def retrieve_map(self):

        map_file = self.map_name in os.listdir(f"{"C:/Users/charl/Documents/Scripts/NexusExplorer/Nexusvault/output/export"}/Map/") #TODO

        if map_file:
            return map_file

        return

# # def _buildQuestObjectives():
# #     """
# #     Link objectives to their quest.
# #     """
# #     quests = loadManager['Quest2']
# #     questObjectives = loadManager['QuestObjective']

# #     for quest in quests.values():
# #         for objectiveId in ['objective0', 'objective01', 'objective02', 'objective03', 'objective04', 'objective05']:
# #             objective = questObjectives.get(quest[objectiveId])

# #             if objective:
# #                 objective['Quest2'] = quest['itemId']

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

# def _buildLocations():
#     """
#     Link all contents to their location
#     """
#     locations = linkDb(loadManager['WorldLocation2'], 'worldlocation', [
#                                                                         loadManager['WorldZone'],
#                                                                         loadManager['Challenge'],
#                                                                         loadManager['Datacube'],
#                                                                         loadManager['PublicEvent'],
#                                                                         # loadManager['PublicEventObjective'],
#                                                                         loadManager['Quest2'],
#                                                                         # loadManager['QuestObjective'],
#                                                                         loadManager['QuestHub'],
#                                                                         loadManager['PathMission']
#                                                                        ]) # 'QuestDirectionEntry' ???
