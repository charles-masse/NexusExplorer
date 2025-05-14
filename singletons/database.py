
import os

import csv

from singletons import settings

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

class DBDict(dict):

    def __init__(self, name):
        super().__init__()

        self.name = name

class LoadManager:
    _instance = None
    _loaded = {settings['language'] : readCSV(settings['language'], '')}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadManager, cls).__new__(cls)
        return cls._instance

    def __getitem__(self, db):

        self.load(db)
            
        return self._loaded[db]

    def load(self, db):

        if db not in self._loaded:
            self._loaded[db] = readCSV(db)
            print(f'Loaded {db}.')

class LocalizedStrings:

    @classmethod
    def __class_getitem__(cls, key):

        string = loadManager[settings['language']].get(key)

        if string:
            string = string.get('Text')
        
            if string != '':
                return string

loadManager = LoadManager()
