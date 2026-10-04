
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStyle,
    QVBoxLayout,
)

from nexus_explorer.ui.extensions import HtmlDelegate, NEWidget
from nexus_explorer.ui.map_viewer import MapViewer

from .utilities import prep_worlds

if TYPE_CHECKING:
    from nexus_explorer.data import LoadingManager

    from .utilities import WorldData

WINDOW_WIDTH = 350

class WorldListItem(QListWidgetItem):
    """Custom list item that contains a world."""
    def __init__(self, world: "WorldData", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.world = world

        self.set_name()

    def set_name(self):
        #Set item name
        world_string = []
        #Id
        world_string.append(f"<b>[{self.world.id}]</b>")
        #Name
        world_string.append(self.world.name or f'<i>"{self.world.name_map}</i>"')
        #Map
        if not self.world.map:
            world_string.append('<b>[No Map]</b>')
        #Map features #TODO make it more accurate
        world_string.append(f'<b>({len(self.world.locations) + len(self.world.zones)})</b>')
        
        self.setText(' '.join(world_string))

class WorldSelectWindow(NEWidget):
    """Display all available worlds and open the selected one in the map viewer."""
    def __init__(self, loading_manager: "LoadingManager"):
        super().__init__()
        
        self.loading_manager = loading_manager
        #Window settings
        self.setWindowTitle("World Select")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        #Size/Pos
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()

        style = self.style()
        if style:
            self.setFixedSize(
                WINDOW_WIDTH,
                geometry.height() - style.pixelMetric(QStyle.PixelMetric.PM_TitleBarHeight)
            )
            self.move(geometry.topLeft())

        layout = QVBoxLayout(self)
        #Add World list
        self.world_list = QListWidget()
        self.delegate = HtmlDelegate(self.world_list)
        self.world_list.setItemDelegate(self.delegate)
        layout.addWidget(self.world_list)
        #Add Load World Button
        self.load_world_button = QPushButton('Load World')
        self.load_world_button.clicked.connect(self._select_world)
        layout.addWidget(self.load_world_button)

        self._populate_world_list()

    def _populate_world_list(self):
        """Populate the world list with worlds with a map or features"""
        worlds = prep_worlds(self.loading_manager)
        for world in worlds:
            world_names = [item.world.name for item in (self.world_list.item(i) for i in range(self.world_list.count()))]
            if (world.map or world.locations or world.zones) and world.name not in world_names:
                self.world_list.addItem(WorldListItem(world))

    def _select_world(self):
        """Load the selected map inside the map viewer"""
        current_item = self.world_list.currentItem()
        if current_item:
            self.popup = MapViewer(self.loading_manager, current_item.world)
            self.popup.showMaximized()
