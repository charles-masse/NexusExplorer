
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
    def __init__(self, worldData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep world id
        self.worldId = worldData['itemId']
        # Set text
        idString = f"<b>[{worldData['itemId']}]</b>"

        nameString = LocalizedStrings[worldData['localizedTextIdName']] or f'<i>"{worldData['assetPath'].split('\\')[-1]}</i>"'
        
        locations = [loc for loc in worldData.get('WorldLocation2', {}).values() if len(loc) > 13]
        locationsString = f'<b>({len(locations)})</b>'

        self.setText(' '.join([idString, nameString, locationsString]))

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
        # Load all Worlds that have a map
        worldList = [world for world in loadManager['World'].values() if world['assetPath'].split('\\')[-1] in os.listdir(f"{settings['gameFiles']}/map/")]
        for world in worldList:
            self.worldListWidget.addItem(WorldListItem(world))
        # Add HTML formating to the list
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
            self.mapScreen = mapViewer.Window(current_item.worldId)
            self.mapScreen.view.showMaximized()
