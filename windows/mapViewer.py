
import pyperclip

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from PIL.ImageQt import ImageQt

from singletons import settings, loadManager

from actions.mapViewer import generateMapImage, clusterLocations, MAP_SIZE, MAP_CHUNK_RESOLUTION

from windows import locationReader

HALF_MAP = int(((MAP_SIZE / 2) * MAP_CHUNK_RESOLUTION))

ICON_SIZE = 32
HALF_SIZE = ICON_SIZE / 2

# def calculateBounds(bounds0, bounds1, bounds2, bounds3):
#     """
#     Calculate the map bounding box
#     """
#     return int(bounds0) * (32 / settings['mapScale']), int(bounds1) * (32 / settings['mapScale']), int(bounds2) * (32 / settings['mapScale']), int(bounds3) * (32 / settings['mapScale'])

def worldCoords(posX, posY):
    """
    Map coords to world coords
    """
    return -int(HALF_MAP - (posX * settings['mapScale'])), -int(HALF_MAP - (posY * settings['mapScale']))

def screenPos(worldX, worldY):
    """
    World coords to map coords
    """
    return (HALF_MAP + float(worldX)) / settings['mapScale'], (HALF_MAP + float(worldY)) / settings['mapScale']

class worldThread(QThread):
    """
    Thread for the loading bar
    """
    setMax = pyqtSignal(int)
    setProgress = pyqtSignal(int)
    worldGenerated = pyqtSignal(object)

    def __init__(self, worldId, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.worldId = worldId

    def run(self):

        def maxCallback(maxValue):
            self.setMax.emit(maxValue)

        def progressCallback(progress):
            self.setProgress.emit(progress)

        for database in ['Creature2', 'VirtualItem', 'Item2', 'TradeskillSchematic2']:
            loadManager.load(database)

        im = generateMapImage(self.worldId, maxCallback, progressCallback)

        self.worldGenerated.emit(im)

class loadingBar(QWidget):
    """
    Simple loading bar
    """
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        layout.addWidget(self.progressBar)

    def setProgress(self, value):
        self.progressBar.setValue(value)

    def setMax(self, value):
        self.progressBar.setMaximum(value)

class LocationObject(QObject):
    """
    A map object that retains feature informations
    """
    clicked = pyqtSignal(QGraphicsPixmapItem)

    def __init__(self, content, posX, posY):
        super().__init__()

        self.content = content

        for type in locationReader.CONTENT_TYPES.keys():
            if type in self.content:

                if type == 'QuestHub':
                    # Faction hubs
                    questFactions = [quest['questPlayerFactionEnum'] for quest in self.content.get('Quest2', {}).values()]
                    
                    if len(set(questFactions)) == 1:
                        factionId = int(questFactions[0])

                    else:
                        factionId = 2

                    path = locationReader.CONTENT_TYPES[type]['icon'][factionId]

                elif type == 'PathMission':
                    # Path missions
                    missionTypes = [mission['pathTypeEnum'] for mission in self.content['PathMission'].values()]
                    missionId = int(max(set(missionTypes), key=missionTypes.count))

                    path = locationReader.CONTENT_TYPES[type]['icon'][missionId]

                else:
                    path = locationReader.CONTENT_TYPES[type]['icon']

                pixmap = QPixmap(f'{settings['gameFiles']}/UI/Icon/{path}').scaled(ICON_SIZE, ICON_SIZE)

                self.icon = LocationIcon(self)
                self.icon.setPixmap(pixmap)
                self.icon.setPos(posX - HALF_SIZE, posY - HALF_SIZE)
                self.icon.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                self.icon.mouseReleaseEvent = self._clickIcon

                break

    def _clickIcon(self, event):
        self.clicked.emit(self.icon)

class LocationIcon(QGraphicsPixmapItem):
    """
    A clickable icon on the map that retains parent and has a glow
    """
    def __init__(self, parent=None, *args, **kwargs):
        super(LocationIcon, self).__init__(*args, **kwargs)

        self.parent = parent

    def paint(self, painter, option, widget=None):

        if self.isSelected():
            pen = QPen(QColor(255, 255, 0, 180), 6)
            painter.setPen(pen)
            painter.drawEllipse(self.boundingRect().adjusted(3, 3, -3, -3))
        # Remove selection box
        option.state &= ~QStyle.StateFlag.State_Selected
        super().paint(painter, option, widget)

class ObjectiveIcon(QGraphicsPixmapItem):

    def __init__(self, objectiveId):
        super().__init__()

        self.pixmap = QPixmap(f'{settings['gameFiles']}/UI/Assets/TexPieces/UI_CRB_HUD_Tracker_349_73/UI_CRB_HUD_Tracker_349_73.png')
        self.setPixmap(self.pixmap)

        self.text = QGraphicsTextItem(str(objectiveId), self)
        self.text.setDefaultTextColor(QColor('white'))
        self.text.setFont(QFont(f'{settings['gameFiles']}/UI/Fonts/segoeuib.ttf', 10))

        textRect = self.text.boundingRect()
        self.text.setPos((self.pixmap.width() / 2) - (textRect.width() / 2), 0)

class Window(QGraphicsScene):
    """
    The map viewer
    """
    def __init__(self, worldId, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.worldId = worldId

        self.view = QGraphicsView(self)
        self.view.setMouseTracking(True)
        self.view.setWindowTitle("Map Viewer")

        self.loadBar = loadingBar()
        self.loadBar.show()
        # Center loading bar
        screenGeometry = QApplication.primaryScreen().availableGeometry()
        loadBarSize = self.loadBar.size()

        x = int((screenGeometry.width() / 2) - (loadBarSize.width() / 2))
        y = int((screenGeometry.height() / 2) - (loadBarSize.height() / 2))

        self.loadBar.move(x, y)
        # Generate world on thread
        self.thread = worldThread(self.worldId)
        self.thread.setMax.connect(self.loadBar.setMax)
        self.thread.setProgress.connect(self.loadBar.setProgress)
        self.thread.worldGenerated.connect(self.drawMap)
        self.thread.run() # Fix this one day

    def drawMap(self, worldIm):
        """
        Display the map when it's done generating/opening
        """
        self.loadBar.close()

        scaledHalf = int(HALF_MAP / settings['mapScale'])
        self.setSceneRect(0, 0, scaledHalf * 2, scaledHalf * 2)
        # Add map to scene (if there's a map)
        if worldIm:
            self.mapQt = ImageQt(worldIm)
            pixMap = QPixmap.fromImage(self.mapQt)
            bgImg = self.addPixmap(pixMap)
        # Cluster features and sort for icon layering
        locations = clusterLocations(loadManager['World'][self.worldId].get('WorldLocation2', {}).values())
        locations.sort(key=lambda index: float(index['position2']))
        # Add locations with content to map
        for location in locations:
            if any(content in locationReader.CONTENT_TYPES.keys() for content in location):
                self.drawLocation(location['position0'], location['position2'], location)
        # Add coords on mouse pointer
        self.coordsText = QGraphicsTextItem()
        self.coordsText.setDefaultTextColor(QColor(79, 204, 60))

        font = QFont()
        font.setBold(True)
        self.coordsText.setFont(font)
        self.addItem(self.coordsText)
        # Center view to world center
        QTimer.singleShot(0, lambda: self.view.centerOn(QPointF(scaledHalf, scaledHalf)))
    # Locations
    def drawLocation(self, worldX, worldY, data):
        """
        Place a location on the map
        """
        location = LocationObject(data, *screenPos(worldX, worldY))
        location.clicked.connect(self.popup)
        self.addItem(location.icon)

    def drawObjective(self, worldX, worldY, objectiveId):
        """
        Place an Objective on the map
        """
        obj = ObjectiveIcon(objectiveId)
        self.addItem(obj)
        position = screenPos(worldX, worldY)
        obj.setPos(position[0] - (obj.pixmap.width() / 2), position[1] - (obj.pixmap.height() / 2))

    def focusOn(self, focus=None):
        """
        Focus on a specific icon on the map and clear objectives
        """
        for item in self.items():

            if isinstance(item, LocationIcon):

                if (not focus or item == focus):
                    item.setOpacity(1.0)
                    
                else:
                    item.setOpacity(0.4)

            elif isinstance(item, ObjectiveIcon):
                self.removeItem(item)
          
    # Mouse coords
    def mouseMoveEvent(self, event):
        """
        Display the map coords on the mouse
        """
        super().mouseMoveEvent(event)

        coords = event.scenePos()
        
        self.mouseX, self.mouseY = worldCoords(coords.x(), coords.y())
        self.coordsText.setPos(coords.x() + 18, coords.y())
        self.coordsText.setHtml(f"<div style='background-color:rgba(24, 25, 23, 100);'>&nbsp;&nbsp;({self.mouseX}, {self.mouseY})&nbsp;</div>")

    def mousePressEvent(self, event):
        """
        Copy the teleport command for the current coords on click to teleport in-game
        """
        super().mousePressEvent(event)

        pyperclip.copy(f"!tele {self.mouseX} 0 {self.mouseY} {self.worldId}")

    def popup(self, locIcon):
        """
        Open the window with current location's content
        """
        self.popup = locationReader.Window(self, locIcon)
        self.popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.popup.show()
