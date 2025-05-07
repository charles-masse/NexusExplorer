
import random

import pyperclip

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from PIL.ImageQt import ImageQt

from singletons import settings

from actions.mapViewer import generateMapImage, clusterLocations, MAP_SIZE, MAP_CHUNK_RESOLUTION

from windows import locationReader

HALF_MAP = int(((MAP_SIZE / 2) * MAP_CHUNK_RESOLUTION))

def calculateBounds(bounds0, bounds1, bounds2, bounds3):
    """
    Calculate the map bound (not used atm)
    """
    return int(bounds0) * (32 / settings['mapScale']), int(bounds1) * (32 / settings['mapScale']), int(bounds2) * (32 / settings['mapScale']), int(bounds3) * (32 / settings['mapScale'])

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

    def __init__(self, world):
        super().__init__()

        self.world = world

    def run(self):

        def maxCallback(maxValue):
            self.setMax.emit(maxValue)

        def progressCallback(progress):
            self.setProgress.emit(progress)

        im = generateMapImage(self.world, maxCallback, progressCallback)
        self.worldGenerated.emit(im)

class loadingBar(QWidget):
    """
    Simple loading bar
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Generating...')

        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        layout.addWidget(self.progressBar)

    def setProgress(self, value):
        self.progressBar.setValue(value)

    def setMax(self, value):
        self.progressBar.setMaximum(value)

class LocationCircle(QObject):
    """
    A clickable circle on the map that retains map features
    """
    clicked = pyqtSignal(dict)

    def __init__(self, locData, color, rect, parent=None):
        super().__init__(parent)
        
        self.locData = locData

        self.graphicsItem = QGraphicsEllipseItem(rect)
        self.graphicsItem.setPen(QPen(color))
        self.graphicsItem.setBrush(QBrush(color))
        self.graphicsItem.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)

        self.graphicsItem.mouseReleaseEvent = self.mouseReleaseEvent

    def mouseReleaseEvent(self, event):
        self.clicked.emit(self.locData)
        QGraphicsEllipseItem.mouseReleaseEvent(self.graphicsItem, event)

class Window(QGraphicsScene):
    """
    The map viewer
    """
    def __init__(self, world, parent=None):
        super().__init__(parent)

        self.world = world
        self.allLocations = []

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
        self.thread = worldThread(self.world)
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
        # Add map to scene
        self.mapQt = ImageQt(worldIm)
        pixMap = QPixmap.fromImage(self.mapQt)
        bgImg = self.addPixmap(pixMap)
        # Add locations to map
        locations = clusterLocations(self.world.get('WorldLocation2', {}).values())
        # locations = self.world['WorldLocation2'].values()
        # pprint(locations)
        for location in locations:
            self.drawLocation(location, location['position0'], location['position2'])
        # Add coords on mouse pointer
        self.coordsText = QGraphicsTextItem()
        self.coordsText.setDefaultTextColor(QColor(79, 204, 60))

        font = QFont()
        font.setBold(True)
        self.coordsText.setFont(font)
        self.addItem(self.coordsText)

        self.view.showMaximized()
        # Center view to world center
        QTimer.singleShot(0, lambda: self.view.centerOn(QPointF(scaledHalf, scaledHalf)))
    # Location circles
    def drawLocation(self, data, worldX, worldY, radius=256, color=None):
        """
        Place a locationCircle to the specified position
        """
        if color == None :
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 200)

        posX, posY = screenPos(worldX, worldY)
        radiusScaled = float(radius) / 10
        halfRadius = radiusScaled / 2

        circle = LocationCircle(data, color, QRectF(posX - halfRadius, posY - halfRadius, radiusScaled, radiusScaled))
        circle.clicked.connect(self.openLocation)
        self.addItem(circle.graphicsItem)

    def openLocation(self, locData):

        self.popup = locationReader.Window(locData)
        self.popup.show()
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

        pyperclip.copy(f"!tele {self.mouseX} 0 {self.mouseY} {self.world['itemId']}")
