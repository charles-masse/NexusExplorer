
import os

import time

import random

import pyperclip

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from PIL import Image
from PIL.ImageQt import ImageQt

from .utilities import WorldMap, chunkCoords, locsToPos, HALF_MAP

__all__ = ['WorldMap', 'chunkCoords' 'locsToPos']

import locationReader

class worldThread(QThread):

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

        im = WorldMap(self.world, maxCallback, progressCallback)
        self.worldGenerated.emit(im)

class loadingBar(QWidget):

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

class locationCircle(QGraphicsEllipseItem):

    def __init__(self, locData, color, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.locData = locData

        self.setPen(QPen(color))
        self.setBrush(QBrush(color))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def mouseReleaseEvent(self, event):
        super(locationCircle, self).mouseReleaseEvent(event)

        self.popup = locationReader.Window(self.locData)

class Window(QGraphicsScene):

    def __init__(self, world, parent=None):
        super().__init__(parent)

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
        self.thread = worldThread(world)
        self.thread.setMax.connect(self.loadBar.setMax)
        self.thread.setProgress.connect(self.loadBar.setProgress)
        self.thread.worldGenerated.connect(self.drawMap)
        self.thread.run() # Fix this one day

    def drawMap(self, generatedWorld):

        # Get the generated map
        self.generatedWorld = generatedWorld

        scaledHalf = int(HALF_MAP / self.generatedWorld.mapScale)
        self.setSceneRect(0, 0, scaledHalf * 2, scaledHalf * 2)

        self.loadBar.close()
        # Add map to scene
        self.mapQt = ImageQt(self.generatedWorld.im)
        pixMap = QPixmap.fromImage(self.mapQt)
        bgImg = self.addPixmap(pixMap)
        # Add locations to map
        for location in self.generatedWorld.locations:
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

    def drawLocation(self, data, worldX, worldY, radius=256, color=None):

        if color == None :
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 200)

        posX, posY = self.generatedWorld.screenPos(worldX, worldY)
        radiusScaled = float(radius) / 10
        halfRadius = radiusScaled / 2

        location = locationCircle(data, color, QRectF(posX - halfRadius, posY - halfRadius, radiusScaled, radiusScaled))
        self.addItem(location)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        coords = event.scenePos()
        
        self.mouseX, self.mouseY = self.generatedWorld.worldCoords(coords.x(), coords.y())

        self.coordsText.setPos(coords.x() + 18, coords.y())
        self.coordsText.setHtml(f"<div style='background-color:rgba(24, 25, 23, 100);'>&nbsp;&nbsp;({self.mouseX}, {self.mouseY})&nbsp;</div>")
    # Save coords to clipboard to teleport in the game
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        pyperclip.copy(f"!tele {self.mouseX} 0 {self.mouseY} {self.generatedWorld.world['itemId']}")
