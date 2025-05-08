
from PyQt6.QtGui import QScreen
from PyQt6.QtCore import QCoreApplication, QTimer, Qt
from PyQt6.QtWidgets import *

from ui import HtmlDelegate
from windows import mapViewer
from singletons import Worlds, LocalizedStrings

WINDOW_WIDTH = 325

class WorldListItem(QListWidgetItem):
    """
    Custom list item that retains world data.

    """
    def __init__(self, worldData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep world data
        self.worldData = worldData
        # Set text
        worldId = f"<b>[{worldData['itemId']}]</b>"
        worldName = LocalizedStrings[worldData['localizedTextIdName']] or f'<i>"{worldData['assetPath'].split('\\')[-1]}</i>"'
        worldLocations = f'<b>({len(worldData.get('WorldLocation2', []))})</b>'

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
        self.setFixedSize(WINDOW_WIDTH, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.x(), screen.y())
        # Main Layout
        layout = QVBoxLayout(self)
        # Add WorldList
        self.worldListWidget = QListWidget()
        worldList = Worlds().data
        for world in worldList.values():
            self.worldListWidget.addItem(WorldListItem(world))
        self.delegate = HtmlDelegate(self.worldListWidget)
        self.worldListWidget.setItemDelegate(self.delegate)
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
