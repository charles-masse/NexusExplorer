
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...data import DBDict, LoadingManager
from ..map_viewer.map_icons import LocationIcon
from .content_display import (
    ContentLabel,
    display_challenge,
    display_datacube,
    display_event,
    display_mission,
    display_quest,
)

WINDOW_WIDTH = 400

class ContentViewerWindow(QWidget):

    def __init__(self, loading_manager: LoadingManager, content: DBDict, icon: LocationIcon | None = None):
        super().__init__()

        self.loading_manager = loading_manager
        self.content = content
        self.icon = icon

        # screen = QScreen.availableGeometry(QApplication.primaryScreen())
        # self.move(screen.x(), screen.y())

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(3)
        #General title vs challenge title
        self.setWindowTitle(content.get('name') or content.get('title') or content.get('short') or '- Unnamed -')

        if content.name == 'Datacube':
            display_datacube(self)

        elif content.name == 'Quest2':
            display_quest(self)

        elif content.name == 'PublicEvent':
            display_event(self)

        elif content.name == 'Challenge':
            display_challenge(self)

        elif content.name == 'PathMission':
            display_mission(self)
            
        else:
            raise TypeError('Cannot parse this data.')
        # Quest directions
        # PathMission, Quest, Challenge
        # test = data.get('questDirectionId') or data.get('questDirectionIdCompletion') or data.get('questDirectionIdActive')

        # if test:
        #     self.addQuestDirections(test, 1)

        self.setFixedWidth(WINDOW_WIDTH)
        # Add floating icons
    #     view = QGraphicsView(self)
    #     view.setStyleSheet("background: transparent; border: 0;")
    #     view.setFixedSize(WINDOW_WIDTH, self.sizeHint().height())
    #     view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    #     scene = QGraphicsScene()
    #     scene.setSceneRect(0, 0, view.width(), view.height())
    #     view.setScene(scene)

    #     heightOffset = 0
    #     objId = 1

    #     for i in range(self.main_layout.count()):
    #         item = self.main_layout.itemAt(i)
    #         widget = item.widget()

    #         if widget.objectName() in ['QuestObjective', 'PublicEventObjective']:
    #             test = mapViewer.ObjectiveIcon(objId)
    #             test.setPos(1, heightOffset)
    #             scene.addItem(test)
    #             objId += 1 

    #         heightOffset += widget.sizeHint().height() + 3
    
    def add_label(self, string_name: str):

        text = self.content.get(string_name)
        if text:
            self.main_layout.addWidget(ContentLabel(text, string_name))

    def showEvent(self, event):
        #Focus on icon
        if self.icon:
            self.icon.map_scene.focus(self.icon)

        super().showEvent(event)

    def closeEvent(self, event):
        #Remove focus from icon
        if self.icon:
            self.icon.map_scene.focus()

        super().closeEvent(event)

    # def addQuestDirections(self, directionId, number):

    #     questDirection = loadManager['QuestDirection'].get(directionId)

    #     if questDirection:
    #         for i in range(16):
    #             entry = loadManager['QuestDirectionEntry'].get(questDirection[f'questDirectionEntryId{str(i).zfill(2)}'])

    #             if entry:
    #                 pos = loadManager['WorldLocation2'].get(entry['worldLocation2Id'])

    #                 if pos:
    #                     self.mapView.drawObjective(pos['position0'], pos['position2'], number)
