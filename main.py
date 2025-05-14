
import sys

from PyQt6.QtGui import QCursor, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication

from windows import worldSelect
from singletons import settings

def main():

    app = QApplication(sys.argv)
    # Add visual theme
    with open('stylesheet.css', 'r') as f:
        app.setStyleSheet(f.read())
    app.setWindowIcon(QIcon(f"{settings['gameFiles']}/UI/Icon/launcher_desktop_icon/launcher_desktop_icon.png"))
    app.setOverrideCursor(QCursor(QPixmap(f"{settings['gameFiles']}/UI/Cursors/Point/Point.png"), hotX=2, hotY=2))

    gui = worldSelect.Window()
    gui.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
