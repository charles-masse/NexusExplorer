
import pyperclip
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ..map import cluster_locations, generate_map

# from . import locationReader

MAP_SIZE = 128
MAP_CHUNK_RESOLUTION = 512
MAP_SCALE = 0.125

HALF_MAP = int((MAP_SIZE / 2) * MAP_CHUNK_RESOLUTION)

ICON_SIZE = 32
HALF_SIZE = ICON_SIZE / 2

# def calculateBounds(bounds0, bounds1, bounds2, bounds3):
#     """Calculate the map bounding box
#     """
#     return int(bounds0) * (32 / settings['mapScale']), int(bounds1) * (32 / settings['mapScale']), int(bounds2) * (32 / settings['mapScale']), int(bounds3) * (32 / settings['mapScale'])

def world_to_screen_pos(world_x, world_y):
    """World coords to map coords
    """
    return (HALF_MAP + float(world_x)) * MAP_SCALE, (HALF_MAP + float(world_y)) * MAP_SCALE

def screen_to_world_pos(pos_x, pos_y):
    """Map coords to world coords
    """
    return -int(HALF_MAP - (pos_x / MAP_SCALE)), -int(HALF_MAP - (pos_y / MAP_SCALE))

class LocationObject(QObject):
    """A map object that retains feature informations
    """
    clicked = pyqtSignal(QGraphicsPixmapItem)

    def __init__(self, game_files, location_data):
        super().__init__()

        self.icon = LocationIcon(self)

        if len(location_data.hubs):
            path = 'Map/Node/Map_QuestHub/Map_QuestHub.png'
             # Faction hubs
            # questFactions = [quest['questPlayerFactionEnum'] for quest in self.content.get('Quest2', {}).values()]
            
            # if len(set(questFactions)) == 1:
            #     factionId = int(questFactions[0])
            # else:
            #     factionId = 2

            # path = locationReader.CONTENT_TYPES[type]['icon'][factionId]

        elif len(location_data.missions):
            path = 'Map/Node/UI_Map_Soldier/UI_Map_Soldier.png'
            # missionTypes = [mission['pathTypeEnum'] for mission in self.content['PathMission'].values()]
            # missionId = int(max(set(missionTypes), key=missionTypes.count))

            # path = locationReader.CONTENT_TYPES[type]['icon'][missionId]

        elif len(location_data.datacubes):
            path = 'Missions/Scientist_DatacubeDiscovery/Scientist_DatacubeDiscovery.png'

        elif len(location_data.events):
            path = 'Map/Node/UI_Map_Events/UI_Map_Events.png'

        elif len(location_data.challenges):
            path = 'Map/Node/UI_Map_Challenges/UI_Map_Challenges.png'

        else:
            path = 'Map/Node/UI_Map_Quests/UI_Map_Quests.png'

        pixmap = QPixmap(f'{game_files}/UI/Icon/{path}').scaled(ICON_SIZE, ICON_SIZE)
        self.icon.setPixmap(pixmap)

        screen_x, screen_y = world_to_screen_pos(*location_data.position)
        self.icon.setPos(screen_x - HALF_SIZE, screen_y - HALF_SIZE)
        
        self.icon.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.icon.mouseReleaseEvent = self.select_location

    def select_location(self, event):
        self.clicked.emit(self.icon)

class LocationIcon(QGraphicsPixmapItem):
    """A clickable icon on the map that retains parent and has a glow effect
    """
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

    def paint(self, painter, option, widget=None):

        if self.isSelected():
            pen = QPen(QColor(255, 255, 0, 180), 6)
            painter.setPen(pen)
            painter.drawEllipse(self.boundingRect().adjusted(3, 3, -3, -3))
        # Remove selection box
        option.state &= ~QStyle.StateFlag.State_Selected

        super().paint(painter, option, widget)

# class ObjectiveIcon(QGraphicsPixmapItem):

#     def __init__(self, objectiveId):
#         super().__init__()

#         self.pixmap = QPixmap(f'{settings['gameFiles']}/UI/Assets/TexPieces/UI_CRB_HUD_Tracker_349_73/UI_CRB_HUD_Tracker_349_73.png')
#         self.setPixmap(self.pixmap)

#         self.text = QGraphicsTextItem(str(objectiveId), self)
#         self.text.setDefaultTextColor(QColor('white'))
#         self.text.setFont(QFont(f'{settings['gameFiles']}/UI/Fonts/segoeuib.ttf', 10))

#         textRect = self.text.boundingRect()
#         self.text.setPos((self.pixmap.width() / 2) - (textRect.width() / 2), 0)

class Window(QGraphicsScene):
    """The map viewer
    """
    def __init__(self, loading_manager, world,):
        super().__init__()

        self.loading_manager = loading_manager
        self.world = world

        self.view = QGraphicsView(self)
        self.view.setMouseTracking(True)
        self.view.setWindowTitle("Map Viewer")

        self.display_map()
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
        scaled_half = int(HALF_MAP * MAP_SCALE)
        self.setSceneRect(0, 0, scaled_half * 2, scaled_half * 2)
        #Add map image to scene (if there's a map)
        if self.world.isMap:
            world_image = generate_map(self.loading_manager.game_files, self.world)
            image_qt = ImageQt(world_image).copy()
            pixMap = QPixmap.fromImage(image_qt)
            self.addPixmap(pixMap)
        #Cluster locations and add them to the map
        locations = cluster_locations(self.world.locations)
        for location in locations:
            self.drawLocation(location)
        #Center view to world center
        self.view.centerOn(QPointF(scaled_half, scaled_half))

    def drawLocation(self, location):
        """Place a location on the map
        """
        location = LocationObject(self.loading_manager.game_files, location)
        # location.clicked.connect(self.popup) #TODO
        self.addItem(location.icon)

    # def drawObjective(self, worldX, worldY, objectiveId):
    #     """Place an Objective on the map
    #     """
    #     obj = ObjectiveIcon(objectiveId)
    #     self.addItem(obj)
    #     position = world_to_screen_pos(worldX, worldY)
    #     obj.setPos(position[0] - (obj.pixmap.width() / 2), position[1] - (obj.pixmap.height() / 2))

    # def focusOn(self, focus=None):
    #     """Focus on a specific icon on the map and clear objectives
    #     """
    #     for item in self.items():

    #         if isinstance(item, LocationIcon):

    #             if (not focus or item == focus):
    #                 item.setOpacity(1.0)
                    
    #             else:
    #                 item.setOpacity(0.4)

    #         elif isinstance(item, ObjectiveIcon):
    #             self.removeItem(item)

    #Mouse coords
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
        super().mousePressEvent(event)

        pyperclip.copy(f"!tele {self.mouse_x} 0 {self.mouse_y} {self.world.id}")

    # def popup(self, locIcon):
    #     """Open the window with current location's content
    #     """
    #     self.popup = locationReader.Window(self, locIcon)
    #     self.popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    #     self.popup.show()
