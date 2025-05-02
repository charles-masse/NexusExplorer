
import sys

import json

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor, QPixmap, QIcon

import worldSelect

class Settings:
    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)

            with open('settings.json') as f:
                cls._instance._data = json.load(f)

        return cls._instance

    def __getitem__(self, key):
        return self._data.get(key)

    def __getattr__(self, key):

        if key in self._data:
            return self._data[key]

settings = Settings()

def main():

    gameFiles = settings['gameFiles']

    app = QApplication(sys.argv)
    # Add visual theme
    app.setOverrideCursor(QCursor(QPixmap(f'{gameFiles}/UI/Cursors/Point/Point.png'), hotX=2, hotY=2))
    app.setWindowIcon(QIcon(f'{gameFiles}/UI/Icon/launcher_desktop_icon/launcher_desktop_icon.png'))
    with open('stylesheet.css', 'r') as f:
        app.setStyleSheet(f.read())

    gui = worldSelect.Window()
    gui.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
