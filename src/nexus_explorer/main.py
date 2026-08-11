
import sys
from pathlib import Path
from PyQt6.QtGui import QCursor, QIcon, QPixmap
from PyQt6.QtWidgets import QApplication
from ui.world_select import WorldSelectWindow


def main():

    app = QApplication(sys.argv)
    # Visual Theme
    with open(f'{Path(__file__).resolve().parent}/stylesheet.css', 'r') as f:
        app.setStyleSheet(f.read())
    # app.setWindowIcon(QIcon(f"{settings['gameFiles']}/UI/Icon/launcher_desktop_icon/launcher_desktop_icon.png"))
    # app.setOverrideCursor(QCursor(QPixmap(f"{settings['gameFiles']}/UI/Cursors/Point/Point.png"), hotX=2, hotY=2))

    gui = WorldSelectWindow()
    gui.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
