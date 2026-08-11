
from model import loadManager
from model.data_types import WorldData
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)
from ui.widgets import HtmlDelegate

# from src.windows import mapViewer

WINDOW_WIDTH = 325

class WorldListItem(QListWidgetItem):
    """Custom list item that contains a world.
    """
    def __init__(self, world, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.world = world

        self.set_world_name()

    def set_world_name(self):

        world_string = []
        #World Id
        world_string.append(f"<b>[{self.world.id}]</b>")
        #World Name or Map Name
        world_string.append(self.world.name or f'<i>"{self.world.map_name}</i>"')
        #Is there a map
        if not self.world.map:
            world_string.append('<b>[No Map]</b>')
        #Map features
        world_string.append(f'<b>({len(self.world.locations)})</b>')
        
        self.setText(' '.join(world_string))

class WorldSelectWindow(QWidget):
    """Display all available worlds and open the selected one in the map viewer.
    """
    def __init__(self):
        super().__init__()
        #Window settings
        self.setWindowTitle("World Select")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        #Size/Pos
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(WINDOW_WIDTH, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.x(), screen.y())

        layout = QVBoxLayout(self)
        #Add World list
        self.world_list = QListWidget()
        self.delegate = HtmlDelegate(self.world_list)
        self.world_list.setItemDelegate(self.delegate)
        layout.addWidget(self.world_list)
        #Add Load Buttom
        load_world_button = QPushButton('Load World')
        load_world_button.released.connect(self._select_map)
        layout.addWidget(load_world_button)

        self._populate_world_list()

    def _populate_world_list(self):
        """Populate the world list with worlds with map or features
        """
        for world in loadManager['World'].values(): #CBB
            world_data = WorldData(**world)
            #Add world to list if world has a map and/or locations
            if world_data.map or len(world_data.locations):
                self.world_list.addItem(WorldListItem(world_data))


    def _select_map(self):
        """Load the selected map inside the map viewer
        """
        current_item = self.world_list.currentItem()
        #If something is selected
        if current_item:
            pass #DELETE
            # self.mapScreen = mapViewer.Window(current_item.world.id)
            # self.mapScreen.view.showMaximized()
