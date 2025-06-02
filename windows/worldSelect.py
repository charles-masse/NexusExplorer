
import os

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ui import HtmlDelegate
from windows import mapViewer
from actions.worldSelect import prepWorlds
from singletons import LocalizedStrings, settings, loadManager

WINDOW_WIDTH = 325

class WorldListItem(QListWidgetItem):
    """
    Custom list item that retains world id.

    """
    def __init__(self, worldId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep world id
        self.worldId = worldId

class Window(QWidget):
    """
    Display all available worlds and open the selected one in the map viewer.
    """
    def __init__(self):
        super().__init__()
        # Window settings
        self.setWindowTitle("World Select")
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(WINDOW_WIDTH, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.x(), screen.y())

        layout = QVBoxLayout(self)
        # Add World list
        self.worldListWidget = QListWidget()
        # Load all Worlds that have a map or features
        for world in loadManager['World'].values():

            worldString = []
            # World Id
            worldId = world['itemId']
            worldString.append(f"<b>[{worldId}]</b>")
            # World Name
            nameString = LocalizedStrings[world['localizedTextIdName']] or f'<i>"{world['assetPath'].split('\\')[-1]}</i>"'
            worldString.append(nameString)
            # Is there a map
            isMap = world['assetPath'].split('\\')[-1] in os.listdir(f"{settings['gameFiles']}/map/")
            if not isMap:
                worldString.append('<b>[No Map]</b>')
            # Map features
            locations = [loc for loc in world.get('WorldLocation2', {}).values() if len(loc) > 13]
            worldString.append(f'<b>({len(locations)})</b>')
            # Add world to list
            if locations or isMap:
                self.worldListWidget.addItem(WorldListItem(worldId, ' '.join(worldString)))
        # Add HTML formating to the list
        self.delegate = HtmlDelegate(self.worldListWidget)
        self.worldListWidget.setItemDelegate(self.delegate)
        layout.addWidget(self.worldListWidget)
        # Add Load Buttom
        loadWorld = QPushButton('Load World')
        loadWorld.released.connect(self._loadMap)
        layout.addWidget(loadWorld)

    def _loadMap(self):
        # If something is selected
        current_item = self.worldListWidget.currentItem()
        if current_item:
            self.mapScreen = mapViewer.Window(current_item.worldId)
            self.mapScreen.view.showMaximized()
