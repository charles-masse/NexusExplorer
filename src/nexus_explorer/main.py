
import sys
from pathlib import Path

from PyQt6.QtGui import QCursor, QIcon, QPixmap
from PyQt6.QtWidgets import QApplication

from .data import LoadingManager, prep_worlds
from .ui import WorldSelectWindow


def main():
    
    game_files = sys.argv[1] if len(sys.argv) > 1 else None

    if game_files == None:
        raise ValueError('Please add the path to the exported game files in your command.\nexemple: nexus_explorer "Nexusvault\\output\\export"')
    #Init loading manager and start prepping the world data
    loading_manager = LoadingManager(game_files)
    prep_worlds(loading_manager)
    #PyQt
    app = QApplication(sys.argv)
    #Visual Theme
    with open(f'{Path(__file__).resolve().parent}/stylesheet.css', 'r') as f:
        app.setStyleSheet(f.read())
    app.setWindowIcon(QIcon(f"{game_files}/UI/Icon/launcher_desktop_icon/launcher_desktop_icon.png"))
    app.setOverrideCursor(QCursor(QPixmap(f"{game_files}/UI/Cursors/Point/Point.png"), hotX=2, hotY=2))

    gui = WorldSelectWindow(loading_manager)
    gui.show()

    sys.exit(app.exec())
