
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStyle,
    QVBoxLayout,
)

from ..data import LoadingManager, WorldData
from .extensions import HtmlDelegate, NEWidget
from .map_viewer import MapViewer

WINDOW_WIDTH = 325

class WorldListItem(QListWidgetItem):
    """Custom list item that contains a world."""
    def __init__(self, world: WorldData, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.world = world

        self.set_world_name()

    def set_world_name(self):
        #TODO get name from continent
        world_string = []
        #World Id
        world_string.append(f"<b>[{self.world.id}]</b>")
        #World Name or Map Name
        world_string.append(self.world.name or f'<i>"{self.world.map_name}</i>"')
        #Is there a map
        if not self.world.isMap:
            world_string.append('<b>[No Map]</b>')
        #Map features #TODO
        # world_string.append(f'<b>({len(self.world.locations)})</b>')
        
        self.setText(' '.join(world_string))

class WorldSelectWindow(NEWidget):
    """Display all available worlds and open the selected one in the map viewer."""
    def __init__(self, loading_manager: LoadingManager):
        super().__init__()
        
        self.loading_manager = loading_manager
        #Window settings
        self.setWindowTitle("World Select")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        #Size/Pos
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        self.setFixedSize(WINDOW_WIDTH, geometry.height() - self.style().pixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(geometry.topLeft())

        layout = QVBoxLayout(self)
        #Add World list
        self.world_list = QListWidget()
        self.delegate = HtmlDelegate(self.world_list)
        self.world_list.setItemDelegate(self.delegate)
        layout.addWidget(self.world_list)
        #Add Load World Buttom
        self.load_world_button = QPushButton('Load World')
        self.load_world_button.released.connect(self._select_map)
        layout.addWidget(self.load_world_button)

        self._populate_world_list(loading_manager['World'])

    def _populate_world_list(self, worlds):
        """Populate the world list with worlds with map or features"""
        for world in worlds.values():
            world_data = WorldData(**world)
            #Can we find the map in the game files
            world_data.isMap = world_data.map_name in os.listdir(f"{self.loading_manager.game_files}/Map/")
            #Add world to list if world has a map and/or zones and is not already in the list
            world_names = [item.world.name or item.world.map_name for item in (self.world_list.item(i) for i in range(self.world_list.count()))]
            if world_data.isMap and world_data.zones: #world_data.isMap or or (world_data.name or world_data.map_name) not in world_names
                self.world_list.addItem(WorldListItem(world_data))

    def _select_map(self):
        """Load the selected map inside the map viewer"""
        current_item = self.world_list.currentItem()
        
        if current_item:
            self.popup = MapViewer(self.loading_manager, current_item.world)
            self.popup.showMaximized()
