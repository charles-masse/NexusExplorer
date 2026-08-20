
import csv
from typing import Self

from . import WorldData


class DBDict(dict):
    """A dictionary that keeps the name of the database
    """
    def __init__(self, name: str, data: dict[str, str] | None = None):
        
        if data:
            super().__init__(data)
        else:
            super().__init__()

        self.name = name

class LoadingManager:
    _instance = None

    def __init__(self, game_files: str, language: str="en-US"):
        self.game_files = game_files
        self.language = language
        #Load language file right away
        self._loaded = {language : self.read_csv(language, '')}
        # Parsed data
        self.worlds: list[WorldData] = []

    def __new__(cls, game_files: str) -> Self:

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __getitem__(self, db_name: str) -> DBDict:

        self.load(db_name)
            
        return self._loaded[db_name]

    def load(self, db_name: str):

        if db_name not in self._loaded:
            self._loaded[db_name] = self.read_csv(db_name)

    def read_csv(self, db_name:str, folder:str='DB') -> DBDict:
        """Read a .csv file
        - db_name: Name of the requested .csv
        - folder: Nexusvault folder where the .csv is stored
        """
        dbDict = DBDict(db_name)

        with open('/'.join([self.game_files, folder, db_name, db_name + '.csv']), encoding='utf') as f:
            #Skip first line
            next(f)

            reader = csv.DictReader(f, delimiter=';')

            keyField = reader.fieldnames[0]
            valueFields = [field for field in reader.fieldnames[1:]]

            for row in reader:
                for field in valueFields:

                    field_name = field.split(' [')[0]
                    #Localize strings #TODO is this smart?
                    if field_name.startswith('localizedTextId'):
                        #Remove 'localizedStringId' from name and lowercase the first letter
                        field_name = field_name.replace('localizedTextId', '')
                        field_name = field_name[0].lower() + field_name[1:]

                        localized_string = self[self.language].get(row[field])

                        if localized_string and localized_string.get('Text') != '':
                            data = localized_string.get('Text')
                        else:
                            data = False

                    else:
                        data = row[field]
                        
                    dbDict.setdefault(row[keyField], {'itemId':row[keyField]}).setdefault(field_name, data)

        return dbDict
