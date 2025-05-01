
import os

import csv

from main import Settings

def linkDb(mainDb, fieldName, refDb):
    """
    Link referenced data ids to the actual data held by another database.

    mainDb (Dict): The database that holds the reference ids and will be returned.
    fieldName (String): Name of the field that contains the reference ids (in mainDb).
    refDb (Dict): Database that contains the data referenced by the ids.
    """
    for dbDict in refDb:
        for itemId, item in dbDict.items():
            for key in [k for k in item if fieldName.lower() in k.lower()]:

                try:
                    mainDb[item[key]].setdefault(dbDict['-1']['dbName'], {})[itemId] = item

                except:
                    pass

    return mainDb

class Worlds:
    """
    Combining all the features of the different worlds into one dictionary.

    Attributes:
        data (dict): All worlds data
    """
    def __init__(self, language='en-US'):
        # Episodes are linked with QuestHubs and worldZone
        self.localizedStrings = self.readCSV(language, '')

        self.datacubes = self.readCSV('Datacube')
        self.zones = self.buildZones()

        self.events, self.eventObjectives = self.buildEvents()

        self.quests, self.questObjectives = self.buildQuests()

        self.questHubs = self.readCSV('QuestHub')

        self.challenges = self.readCSV('Challenge')

        self.locations = self.buildLocations()

        self.data = self.buildWorlds()

    def readCSV(self, db, folder='DB'):
        """
        Read a .csv file and replace the localized text into readable strings.

        db (String): Name of the requested .csv
        folder (String): Nexusvault folder where the .csv is stored
        """
        dbDict = {'-1':{'dbName':db}}

        self.gameFiles = Settings()['gameFiles']
        with open('/'.join([self.gameFiles, folder, db, db + '.csv']).replace('//', '/'), encoding='utf') as f:
            next(f) # Start at line 2 for col names

            reader = csv.DictReader(f, delimiter=';')
            fieldnames = reader.fieldnames

            for row in reader:
                for field in fieldnames[1:]:
                    # Replace string Id by localized text
                    if 'localizedTextId' in field:

                        try:
                            data = self.localizedStrings[row[field]]['Text']

                        except:
                            data = ''

                    else:
                        data = row[field]

                    dbDict.setdefault(row[fieldnames[0]], {'itemId':row[fieldnames[0]]}).setdefault(field.split(' [')[0], data)

        return dbDict

    def buildZones(self):
        """
        Link Datacubes to their zone.
        """
        zones = self.readCSV('WorldZone')

        for cube in self.datacubes.values():

            try:
                zones[cube['worldZoneId']].setdefault('Datacube', {})[cube['itemId']] = cube

            except:
                pass

        return {zones[zone]['itemId']:zones[zone] for zone in zones if zone != '-1' and (zones[zone]['localizedTextIdName'] or 'Datacube' in zones[zone])}

    def buildEvents(self):
        """
        Link objectives to their event.
        """
        events = self.readCSV('PublicEvent')
        eventObjectives = self.readCSV('PublicEventObjective')

        for objective in eventObjectives.values():

            try:
                events[objective['publicEventId']].setdefault('PublicEventObjective', {})[objective['itemId']] = objective
                objective['publicEventId'] = events[objective['publicEventId']]

            except:
                pass

        return events, eventObjectives

    def buildQuests(self):
        """
        Link quest to their objective.
        """
        quests = self.readCSV('Quest2')
        questObjectives = self.readCSV('QuestObjective')

        for quest in quests.values():
            for key in [key for key in quest if 'objective' in key]:

                try:
                    quest[key] = questObjectives[quest[key]]
                    questObjectives[quest[key]['itemId']]['Quest2'] = quest

                except:
                    pass

        return quests, questObjectives

    def buildLocations(self):
        """
        Link all content to their location.
        """
        locations = linkDb(self.readCSV('WorldLocation2'), 'worldlocation', [self.challenges, self.datacubes, self.events, self.eventObjectives, self.quests, self.questHubs, self.questObjectives])
        locations = linkDb(locations, 'worldlocation2idexit', [self.zones])
        
        return {location['itemId']:location for location in locations.values() if len(location) > 13}

    def buildWorlds(self):
        """
        Link location to their world.
        """
        worlds = self.readCSV('World')

        for location in self.locations:

            try:
                worlds[self.locations[location]['worldId']].setdefault('WorldLocation2', {})[location] = self.locations[location]
            
            except:
                pass

        return {worlds[world]['itemId']:worlds[world] for world in worlds if world != '-1' and worlds[world]['assetPath'].split('\\')[-1] in os.listdir(f'{self.gameFiles}/map/')}
