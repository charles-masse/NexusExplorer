
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .content_display import (
    display_challenge,
    display_datacube,
    display_event,
    display_mission,
    display_quest,
)

# from src.actions.links import linkGameObject

WINDOW_WIDTH = 400

class ContentViewerWindow(QWidget):

    def __init__(self, loading_manager, content, icon):
        super().__init__()

        self.loading_manager = loading_manager
        self.icon = icon

        # screen = QScreen.availableGeometry(QApplication.primaryScreen())
        # self.move(screen.x(), screen.y())

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(3)
        #General title vs challenge title
        self.setWindowTitle(content.get('name') or content.get('title') or content.get('short') or '- Unnamed -')

        if content.name == 'Datacube':
            widgets = display_datacube(content)

        elif content.name == 'Quest2':
            widgets = display_quest(content)

        elif content.name == 'PublicEvent':
            widgets = display_event(loading_manager, content)

        elif content.name == 'Challenge':
            widgets = display_challenge(content)

        elif content.name == 'PathMission':
            widgets = display_mission(content)
            
        else:
            raise TypeError('Cannot parse this data.')

    #     # Quest directions
    #     # PathMission, Quest, Challenge
    #     test = data.get('questDirectionId') or data.get('questDirectionIdCompletion') or data.get('questDirectionIdActive')

    #     if test:
    #         self.addQuestDirections(test, 1)

        for widget in widgets:
            self.layout.addWidget(widget)

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

    #     for i in range(self.layout.count()):
    #         item = self.layout.itemAt(i)
    #         widget = item.widget()

    #         if widget.objectName() in ['QuestObjective', 'PublicEventObjective']:
    #             test = mapViewer.ObjectiveIcon(objId)
    #             test.setPos(1, heightOffset)
    #             scene.addItem(test)
    #             objId += 1 

    #         heightOffset += widget.sizeHint().height() + 3
    
    def showEvent(self, event):
        #Focus on icon
        self.icon.parent.focus(self.icon)

        super().showEvent(event)

    def closeEvent(self, event):
        #Remove focus from icon
        self.icon.parent.focus()

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
