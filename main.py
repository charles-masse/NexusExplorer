
import sys

import json

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor, QPixmap, QIcon

import worldSelect

from main import Settings

def Settings():
    # Load settings
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    return settings

def main():
    gameFiles = Settings()['gameFiles']

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
