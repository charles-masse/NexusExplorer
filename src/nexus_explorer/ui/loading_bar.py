
# class loadingBar(QWidget):
#     """Simple loading bar
#     """
#     def __init__(self):
#         super().__init__()

#         layout = QVBoxLayout(self)

#         self.progressBar = QProgressBar()
#         self.progressBar.setTextVisible(False)
#         layout.addWidget(self.progressBar)

#     def setProgress(self, value):
#         self.progressBar.setValue(value)

#     def setMax(self, value):
#         self.progressBar.setMaximum(value)

# self.loadBar = loadingBar()
# self.loadBar.show()
# Center loading bar
# screenGeometry = QApplication.primaryScreen().availableGeometry()
# loadBarSize = self.loadBar.size()

# x = int((screenGeometry.width() / 2) - (loadBarSize.width() / 2))
# y = int((screenGeometry.height() / 2) - (loadBarSize.height() / 2))

# self.loadBar.move(x, y)


# class worldThread(QThread):
#     """Thread for the loading bar
#     """
#     setMax = pyqtSignal(int)
#     setProgress = pyqtSignal(int)
#     worldGenerated = pyqtSignal(object)

#     def __init__(self, worldId, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.worldId = worldId

#     def run(self):

#         def maxCallback(maxValue):
#             self.setMax.emit(maxValue)

#         def progressCallback(progress):
#             self.setProgress.emit(progress)

#         for database in ['Creature2', 'VirtualItem', 'Item2', 'TradeskillSchematic2']:
#             loadManager.load(database)

#         im = generateMapImage(self.worldId, maxCallback, progressCallback)

#         self.worldGenerated.emit(im)

#Generate world on thread
# self.thread = worldThread(self.worldId)
# self.thread.setMax.connect(self.loadBar.setMax)
# self.thread.setProgress.connect(self.loadBar.setProgress)
# self.thread.worldGenerated.connect(self.drawMap)
# self.thread.run()
# self.loadBar.close()