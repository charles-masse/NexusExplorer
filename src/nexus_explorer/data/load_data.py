
import csv
import re


class DBDict(dict):

    def __init__(self, name):
        super().__init__()

        self.name = name

class LoadingManager:
    _instance = None

    def __init__(self, game_files):
        self.game_files = game_files
        #Load language file right away
        self._loaded = {"en-US" : self.read_csv("en-US", '')} #TODO
        # Parsed data
        self.worlds = []

    def __new__(cls, game_files):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __getitem__(self, db):

        self.load(db)
            
        return self._loaded[db]

    def load(self, db):

        if db not in self._loaded:
            self._loaded[db] = self.read_csv(db)

    def read_csv(self, dbName, folder='DB'):
        """Read a .csv file

        db (String): Name of the requested .csv
        folder (String): Nexusvault folder where the .csv is stored
        """
        dbDict = DBDict(dbName)

        with open('/'.join([self.game_files, folder, dbName, dbName + '.csv']), encoding='utf') as f:
            #Skip first line
            next(f) 

            reader = csv.DictReader(f, delimiter=';')

            keyField = reader.fieldnames[0]
            valueFields = [field for field in reader.fieldnames[1:]]

            for row in reader:
                for field in valueFields:

                    field_name = field.split(' [')[0]
                    #Localize strings #TODO is this smart?
                    if field_name.startswith('localized'):

                        field_name = field_name.split('Id')[-1].lower()
                        localized_string = self["en-US"].get(row[field]) #TODO

                        if localized_string and localized_string.get('Text') != '':
                            data = localized_string.get('Text')
                        else:
                            data = False

                    else:
                        data = row[field]
                        
                    dbDict.setdefault(row[keyField], {'itemId':row[keyField]}).setdefault(field_name, data)

        return dbDict

DATABASES = {
             'creature' : 'Creature2',
             'vitem' : 'VirtualItem',
             'item' : 'Item2',
             'schematic' : 'TradeskillSchematic2',
             'quest' : 'Quest2'
            }


# def link_game_object(text):

#     for match in re.finditer(r'(?:<text[^>]*?>)?\$\S*?\((\w+)=(\d+)\)|\$(\w+)=(\d+)(?:</text>)?', text):

#         fullMath = match.group(0)
#         key = match.group(1) or match.group(3)
#         idValue = match.group(2) or match.group(4)

#         linked = loadManager[DATABASES[key.lower()]].get(idValue)
        
#         if linked:
#             linkedText = LocalizedStrings[linked.get('localizedTextIdName')]
            
#         else:
#             linkedText = None

#         if not linkedText:
#             linkedText = f"Can't find {key} id:{idValue}"

#         text = text.replace(fullMath, f'<b><a style="color: rgb(125, 251, 182);" href="{linked}">{linkedText}</a></b>')

#     return text
