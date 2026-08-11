

import csv
import re

# from .settings import settings

DATABASES = {
             'creature' : 'Creature2',
             'vitem' : 'VirtualItem',
             'item' : 'Item2',
             'schematic' : 'TradeskillSchematic2',
             'quest' : 'Quest2'
            }


def read_csv(dbName, folder='DB'):
    """Read a .csv file

    db (String): Name of the requested .csv
    folder (String): Nexusvault folder where the .csv is stored
    """
    dbDict = DBDict(dbName)

    with open('/'.join(["C:/Users/charl/Documents/Scripts/NexusExplorer/Nexusvault/output/export/", folder, dbName, dbName + '.csv']).replace('//', '/'), encoding='utf') as f: # settings['gameFiles']
        next(f) # Skip first line

        reader = csv.DictReader(f, delimiter=';')

        keyField = reader.fieldnames[0]
        valueFields = [field for field in reader.fieldnames[1:]]

        for row in reader:
            for field in valueFields:
                dbDict.setdefault(row[keyField], {'itemId':row[keyField]}).setdefault(field.split(' [')[0], row[field])

    return dbDict

class DBDict(dict):

    def __init__(self, name):
        super().__init__()

        self.name = name

class LoadManager:
    _instance = None
    _loaded = {"en-US" : read_csv("en-US", '')} # settings['language']

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __getitem__(self, db):

        self.load(db)
            
        return self._loaded[db]

    def load(self, db):

        if db not in self._loaded:
            self._loaded[db] = read_csv(db)
            print(f'Loaded {db}.') # DELETE

class LocalizedStrings:

    @classmethod
    def __class_getitem__(cls, key):

        string = loadManager["en-US"].get(key) # settings['language']

        if string:
            string = string.get('Text')
        
            if string != '':
                return string

def link_game_object(text):

    for match in re.finditer(r'(?:<text[^>]*?>)?\$\S*?\((\w+)=(\d+)\)|\$(\w+)=(\d+)(?:</text>)?', text):

        fullMath = match.group(0)
        key = match.group(1) or match.group(3)
        idValue = match.group(2) or match.group(4)

        linked = loadManager[DATABASES[key.lower()]].get(idValue)
        
        if linked:
            linkedText = LocalizedStrings[linked.get('localizedTextIdName')]
            
        else:
            linkedText = None

        if not linkedText:
            linkedText = f"Can't find {key} id:{idValue}"

        text = text.replace(fullMath, f'<b><a style="color: rgb(125, 251, 182);" href="{linked}">{linkedText}</a></b>')

    return text

# Create instance
loadManager = LoadManager()
