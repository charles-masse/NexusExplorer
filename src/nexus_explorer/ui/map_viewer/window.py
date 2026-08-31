
import pyperclip
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import (
    QCloseEvent,
    QColor,
    QFont,
    QPixmap,
    QPolygonF,
)
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QGraphicsTextItem,
    QGraphicsView,
)

from ...constants import HALF_MAP, MAP_SCALE
from ...data import LoadingManager, LocationData, WorldData
from ...map import cluster_locations, generate_map
from . import LocationObject, ObjectiveObject, RegionObject
from .utilities import (
    hex_to_world_coordinates,
    screen_to_world_coordinates,
    world_to_screen_pos,
)

SCALED_HALF = int(HALF_MAP * MAP_SCALE)

class MapScene(QGraphicsScene):

    def __init__(self, loading_manager, world, parent=None):
        super().__init__(parent)

        self.loading_manager = loading_manager
        self.world = world

        self.popup = None

        self.setSceneRect(0, 0, SCALED_HALF * 2, SCALED_HALF * 2)
        #Display the map in the view (if there's a map)
        if world.isMap:
            pixmap = self.display_map()
            self.addPixmap(pixmap)
        #Add coords on mouse pointer
        self.coords_text = QGraphicsTextItem()
        self.coords_text.setDefaultTextColor(QColor(79, 204, 60))
        font = QFont(f'{loading_manager.game_files}/UI/Fonts/segoeuib.ttf', 10)
        font.setBold(True)
        self.coords_text.setFont(font)
        self.addItem(self.coords_text)
        #Objects
        self.display_locations(world.locations)
        self.display_regions(loading_manager)
    
    def display_locations(self, locations):
        #Cluster locations and add them to the map
        locations = cluster_locations(locations)
        for location in locations:
            self.draw_location(location)

    def display_map(self) -> QPixmap:
        """Display the map when it's done generating/loading."""
        world_image = generate_map('/'.join([self.loading_manager.game_files, self.world.map_path.replace('\\', '/')]))
        image_qt = ImageQt(world_image).copy()
        pixmap = QPixmap.fromImage(image_qt)

        return pixmap

    def display_regions(self, loading_manager):

        zones = loading_manager['MapZone']

        for zone in zones.values():
            if zone['mapContinentId'] == 6: #Get from continent

                testA, testB = world_to_screen_pos(*hex_to_world_coordinates(zone['hexMinX'], zone['hexMinY']))
                testC, testD = world_to_screen_pos(*hex_to_world_coordinates(zone['hexLimX'], zone['hexLimY']))

                if zone['flags'] == 0:
                    poly = QPolygonF([QPointF(testA, testB), QPointF(testC, testB), QPointF(testC, testD), QPointF(testA, testD)])
                    self.draw_region(poly)
    
    def draw_location(self, location: LocationData): #TODO x, y
        """Place a location on the map."""
        location_obj = LocationObject(location, self)
        location_obj.clicked.connect(self.select_location)
        self.addItem(location_obj)

    def draw_region(self, region):
        """Draw a region on the map."""
        region_obj = RegionObject(region)
        self.addItem(region_obj)

    def drawObjective(self, x: float, y: float, objective_id: int):
        """Place an Objective on the map"""
        obj = ObjectiveObject(objective_id, self.loading_manager.game_files)
        position = world_to_screen_pos(x, y) #TODO include in icon class
        obj.setPos(position[0] - (obj.im.width() / 2), position[1] - (obj.im.height() / 2))
        self.addItem(obj)

    def focus(self, focus:LocationObject | None = None):
        """Focus on a specific icon on the map and clear objectives."""
        for item in self.items():

            if isinstance(item, LocationObject):

                if (not focus or item == focus):
                    item.setOpacity(1.0)
                else:
                    item.setOpacity(0.4)

            elif isinstance(item, ObjectiveObject):
                self.removeItem(item)

    def select_location(self, icon: LocationObject):
        """Open the window with current location's content"""
        from .. import ContentSelectWindow  #TODO

        self.popup = ContentSelectWindow(self.loading_manager, icon)
        self.popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.popup.show()
        #Defocus from previous focus
        self.focus()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent | None):
        """Display the map coords on the mouse"""
        super().mouseMoveEvent(event)

        if event != None:
            coords = event.scenePos()
            self.mouse_x, self.mouse_y = screen_to_world_coordinates(coords.x(), coords.y())
            self.coords_text.setPos(coords.x() + 11, coords.y() + 1)
            self.coords_text.setHtml(f"<div style='background-color:rgba(24, 25, 23, 100);'>&nbsp;&nbsp;({self.mouse_x}, {self.mouse_y})&nbsp;</div>")

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None):
        """Copy the teleport command for the current coords on click to teleport in-game"""
        pyperclip.copy(f"!tele {self.mouse_x} 0 {self.mouse_y} {self.world.id}")
        super().mousePressEvent(event)

class MapViewer(QGraphicsView):

    def __init__(self, loading_manager: LoadingManager, world: WorldData, parent: QGraphicsScene | None = None):

        self.map_scene = MapScene(loading_manager, world)

        super().__init__(self.map_scene)

        self.setMouseTracking(True)
        self.setWindowTitle("Map Viewer")
        #Center view to world center
        self.centerOn(QPointF(SCALED_HALF, SCALED_HALF))

    def closeEvent(self, event: QCloseEvent | None):
        # #Remove focus from icon
        if self.map_scene.popup:
            self.map_scene.popup.close()

        super().closeEvent(event)
