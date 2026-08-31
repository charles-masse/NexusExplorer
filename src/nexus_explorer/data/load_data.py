
import csv
from typing import Self

from . import WorldData


class DBDict(dict):
    """A dictionary that keeps the name of the database"""
    def __init__(self, name: str, data: dict[str, str] | None = None, **kwargs):
        
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
        new_dict = DBDict(db_name)

        with open('/'.join([self.game_files, folder, db_name, db_name + '.csv']), encoding='utf') as f:
            #Skip first line
            next(f)

            reader = csv.DictReader(f, delimiter=';')

            id_field = reader.fieldnames[0]
            value_fields = [field for field in reader.fieldnames[1:]]

            for row in reader:

                try:
                    new_entry = {'id':int(row[id_field])}

                    for field in value_fields:

                        split_field = field.split(' [')
                        field_name = split_field[0]
                        #Localize strings
                        if field_name.startswith('localizedTextId'):

                            localized_string = self[self.language].get(int(row[field]))

                            if localized_string:
                                data = localized_string.get('Text')
                            else:
                                data = ''
                        #Convert value to the right type
                        elif split_field[-1] not in ['Text', '']:

                            field_type = split_field[-1].split(' ')[0]

                            if field_type == "FLOAT":
                                data = float(row[field])

                            elif field_type == "INT32":
                                data = int(row[field])

                            elif field_type == "BOOL":
                                data = bool(row[field])

                            elif field_type == "STRING":
                                data = row[field]

                            else:
                                print(f'[LoadingManager] Cannot convert data to data type "{field_type}"')

                        else:
                            data = row[field]

                        new_entry.setdefault(field_name, data)
                    #Cleanup data with no human readable strings
                    localized_values = [value for field, value in new_entry.items() if field.startswith('localizedTextId')]

                    if db_name == 'World' or not localized_values or any(value.strip() != '' for value in localized_values):
                        new_dict.setdefault(int(row[id_field]), new_entry)

                except ValueError:
                    print(f'[LoadingManager][{db_name}] "{row[id_field]}" is not a valid Id. -SKIPPED-')

        return new_dict
