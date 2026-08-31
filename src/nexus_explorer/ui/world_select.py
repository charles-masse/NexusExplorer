
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
        #Map features
        world_string.append(f'<b>({len(self.world.locations)})</b>')
        
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

        self._populate_world_list()

    def _populate_world_list(self):
        """Populate the world list with worlds with map or features"""
        #Skip duplicates
        worlds = self.loading_manager.worlds
        for world in [w for w in worlds if (w.name or w.map_name) not in [w.name or w.map_name for w in worlds] or w.locations]:
            self.world_list.addItem(WorldListItem(world))

    def _select_map(self):
        """Load the selected map inside the map viewer"""
        current_item = self.world_list.currentItem()
        if current_item:
            self.popup = MapViewer(self.loading_manager, current_item.world)
            self.popup.showMaximized()
