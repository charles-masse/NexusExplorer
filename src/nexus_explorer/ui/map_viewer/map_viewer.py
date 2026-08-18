
import pyperclip
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...constants import HALF_MAP, MAP_SCALE
from ...map import cluster_locations, generate_map
from ..content_select import ContentSelectWindow
from .map_icons import LocationObject
from .utilities import screen_to_world_pos


class MapViewerWindow(QGraphicsScene):
    """The map viewer
    """
    def __init__(self, loading_manager, world):
        super().__init__()

        self.loading_manager = loading_manager
        self.world = world

        self.view = QGraphicsView(self)
        self.view.setMouseTracking(True)
        self.view.setWindowTitle("Map Viewer")

        scaled_half = int(HALF_MAP * MAP_SCALE)
        self.setSceneRect(0, 0, scaled_half * 2, scaled_half * 2)
        #Display the map in the view (if there's a map)
        if self.world.isMap:
            pixmap = self.display_map()
            self.addPixmap(pixmap)
        #Cluster locations and add them to the map
        locations = cluster_locations(self.world.locations)
        for location in locations:
            self.draw_location(location)
        #Center view to world center
        self.view.centerOn(QPointF(scaled_half, scaled_half))
        #Add coords on mouse pointer
        self.coords_text = QGraphicsTextItem()
        self.coords_text.setDefaultTextColor(QColor(79, 204, 60))
        font = QFont()
        font.setBold(True)
        self.coords_text.setFont(font)
        self.addItem(self.coords_text)

    def display_map(self):
        """Display the map when it's done generating/opening
        """
        world_image = generate_map('/'.join([self.loading_manager.game_files, self.world.map_path.replace('\\', '/')]))
        image_qt = ImageQt(world_image).copy()
        pixmap = QPixmap.fromImage(image_qt)

        return pixmap

    def draw_location(self, location):
        """Place a location on the map
        """
        location_obj = LocationObject(location, self)
        location_obj.clicked.connect(self.select_location)
        self.addItem(location_obj)

    # def drawObjective(self, worldX, worldY, objectiveId):
    #     """Place an Objective on the map
    #     """
    #     obj = ObjectiveIcon(objectiveId)
    #     self.addItem(obj)
    #     position = world_to_screen_pos(worldX, worldY)
    #     obj.setPos(position[0] - (obj.pixmap.width() / 2), position[1] - (obj.pixmap.height() / 2))

    def focus(self, focus=None):
        """Focus on a specific icon on the map and clear objectives
        """
        for item in self.items():

            if isinstance(item, LocationObject):

                if (not focus or item == focus):
                    item.setOpacity(1.0)
                else:
                    item.setOpacity(0.4)

            # elif isinstance(item, ObjectiveIcon):
            #     self.removeItem(item)

    def mouseMoveEvent(self, event):
        """Display the map coords on the mouse
        """
        super().mouseMoveEvent(event)

        coords = event.scenePos()
        self.mouse_x, self.mouse_y = screen_to_world_pos(coords.x(), coords.y())
        self.coords_text.setPos(coords.x() + 18, coords.y())
        self.coords_text.setHtml(f"<div style='background-color:rgba(24, 25, 23, 100);'>&nbsp;&nbsp;({self.mouse_x}, {self.mouse_y})&nbsp;</div>")

    def mousePressEvent(self, event):
        """Copy the teleport command for the current coords on click to teleport in-game
        """
        pyperclip.copy(f"!tele {self.mouse_x} 0 {self.mouse_y} {self.world.id}")
        super().mousePressEvent(event)

    def select_location(self, icon):
        """Open the window with current location's content
        """
        self.content_select = ContentSelectWindow(self.loading_manager, icon)
        self.content_select.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.content_select.show()
