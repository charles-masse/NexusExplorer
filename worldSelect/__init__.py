
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from .utilities import Worlds, linkDb
__all__ = ['worlds', 'linkDb']

import mapViewer

class WorldListItem(QListWidgetItem):
    """
    Custom list item that retains world data.

    """
    def __init__(self, worldData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep world data
        self.worldData = worldData
        # Set text
        worldId = f'[{worldData['itemId']}]'
        worldName = worldData['localizedTextIdName'] or f'"{worldData['assetPath'].split('\\')[-1]}"'
        worldLocations = f'({len(worldData.get('WorldLocation2', []))})'

        self.setText(' '.join([worldId, worldName, worldLocations]))

class Window(QWidget):
    """
    Display all available worlds and open the selected one in the map viewer.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Window settings
        self.setWindowTitle("World Select")
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.move(screen.x(), screen.y())
        self.setFixedSize(350, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        # Main Layout
        layout = QVBoxLayout(self)
        # Add WorldList
        self.worldListWidget = QListWidget()
        worldList = Worlds().data
        for world in worldList.values():
            self.worldListWidget.addItem(WorldListItem(world))
        layout.addWidget(self.worldListWidget)
        # Add Load Buttom
        loadWorld = QPushButton('Load World')
        loadWorld.released.connect(self._loadMap)
        layout.addWidget(loadWorld)

    def _loadMap(self):

        current_item = self.worldListWidget.currentItem()
        # If something is selected
        if current_item:
            mapViewer.Window(current_item.worldData)
