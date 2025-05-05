
import json

class Settings:
    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)

            with open('settings.json') as f:
                cls._instance._data = json.load(f)

        return cls._instance

    def __getitem__(self, key):

        if key in self._data:
            return self._data[key]

        else:
            raise AttributeError(f"Cannot find setting '{key}'")

settings = Settings()
