
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QScreen

from singletons import Worlds, localizedStrings
from windows import mapViewer

class WorldListItem(QListWidgetItem):
    """
    Custom list item that retains world data.

    """
    def __init__(self, worldData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep world data
        self.worldData = worldData
        # Set text
        worldId = f"[{worldData['itemId']}]"
        worldName = localizedStrings[worldData['localizedTextIdName']] or worldData['assetPath'].replace('\\', '/')
        worldLocations = f'({len(worldData.get('WorldLocation2', []))})'

        self.setText(' '.join([worldId, worldName, worldLocations]))

class Window(QWidget):
    """
    Display all available worlds and open the selected one in the map viewer.
    """
    def __init__(self):
        super().__init__()
        # Window settings
        self.setWindowTitle("World Select")
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(350, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.x(), screen.y())
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
