
import os

import csv

from singletons import settings

class DBDict(dict):

    def __init__(self, name):
        super().__init__()

        self.name = name

def readCSV(dbName, folder='DB'):
    """
    Read a .csv file

    db (String): Name of the requested .csv
    folder (String): Nexusvault folder where the .csv is stored
    """
    dbDict = DBDict(dbName)

    with open('/'.join([settings['gameFiles'], folder, dbName, dbName + '.csv']).replace('//', '/'), encoding='utf') as f:
        next(f) # Skip first line

        reader = csv.DictReader(f, delimiter=';')

        keyField = reader.fieldnames[0]
        valueFields = [field for field in reader.fieldnames[1:]]

        for row in reader:
            for field in valueFields:
                dbDict.setdefault(row[keyField], {'itemId':row[keyField]}).setdefault(field.split(' [')[0], row[field])

    return dbDict

class LoadManager:
    _instance = None
    _loaded = {settings['language'] : readCSV(settings['language'], '')}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadManager, cls).__new__(cls)
        return cls._instance

    def __getitem__(self, db):

        if db not in self._loaded:
            self._loaded[db] = readCSV(db)
            print(f'Loaded {db}.')

        return self._loaded[db]

loadManager = LoadManager()

class LocalizedStrings:

    @classmethod
    def __class_getitem__(cls, key):

        string = loadManager[settings['language']].get(key)

        if string:
            string = string.get('Text')
        
            if string != '':
                return string

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

                try:
                    linkDb[item[key]].setdefault(db.name, {})[itemId] = item

                except:
                    continue

    return linkDb

class Worlds:
    """
    Combining all the features of the different worlds into one dictionary.

    Attributes:
        data (dict): All worlds data
    """
    def __init__(self):
        # Episodes are linked with QuestHubs and worldZone
        self.zones = self._buildZones()
        # self.events, self.eventObjectives = self._buildEvents()
        # self.quests, self.questObjectives = self._buildQuests()
        self.locations = self._buildLocations()
        self.data = self._buildWorlds()

    def _buildZones(self):
        """
        Link Datacubes to their zone.
        """
        zones = readCSV('WorldZone')

        for cube in loadManager['Datacube'].values():

            try:
                zones[cube['worldZoneId']].setdefault('Datacube', {})[cube['itemId']] = cube

            except:
                pass

        return {zones[zone]['itemId']:zones[zone] for zone in zones if 'Datacube' in zones[zone]}

        return zones

    # def _buildEvents(self):
    #     """
    #     Link objectives to their event.
    #     """
    #     events = readCSV('PublicEvent')
    #     eventObjectives = readCSV('PublicEventObjective')

    #     for objective in eventObjectives.values():

    #         try:
    #             events[objective['publicEventId']].setdefault('PublicEventObjective', {})[objective['itemId']] = objective
    #             objective['publicEventId'] = events[objective['publicEventId']]

    #         except:
    #             pass

    #     return events, eventObjectives

    # def _buildQuests(self):
    #     """
    #     Link quest to their objective.
    #     """
    #     quests = readCSV('Quest2')
    #     questObjectives = readCSV('QuestObjective')

    #     for quest in quests.values():
    #         for key in [key for key in quest if 'objective' in key]:

    #             try:
    #                 quest[key] = questObjectives[quest[key]]
    #                 questObjectives[quest[key]['itemId']]['Quest2'] = quest

    #             except:
    #                 pass

    #     return quests, questObjectives

    def _buildLocations(self):
        """
        Link all content to their location.
        """
        locations = linkDb(readCSV('WorldLocation2'), 'worldlocation', [self.zones, loadManager['Challenge'], loadManager['Datacube'], loadManager['PublicEvent'], loadManager['Quest2'], loadManager['QuestHub']]) # self.eventObjectives, self.questObjectives
        locations = linkDb(locations, 'worldlocation2idexit', [self.zones])
        
        return {location['itemId']:location for location in locations.values() if len(location) > 13}

    def _buildWorlds(self):
        """
        Link location to their world.
        """
        worlds = readCSV('World')

        for location in self.locations:

            try:
                worlds[self.locations[location]['worldId']].setdefault('WorldLocation2', {})[location] = self.locations[location]
            
            except:
                print('test')
                pass

        return {worlds[world]['itemId']:worlds[world] for world in worlds if worlds[world]['assetPath'].split('\\')[-1] in os.listdir(f'{settings['gameFiles']}/map/')}
