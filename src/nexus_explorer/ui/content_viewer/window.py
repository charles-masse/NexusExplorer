
from pprint import pprint
from typing import TYPE_CHECKING

from PyQt6.QtGui import QCloseEvent, QShowEvent
from PyQt6.QtWidgets import QVBoxLayout

from nexus_explorer.data.utilities import link_referenced
from nexus_explorer.ui.extensions import NEWidget

from .labels import (
    ContentLabel,
    display_challenge,
    display_datacube,
    display_event,
    display_mission,
    display_quest,
)

if TYPE_CHECKING:
    from nexus_explorer.data import LoadingManager
    from nexus_explorer.ui.map_viewer.objects import LocationObject
        

WINDOW_WIDTH = 375

class ContentViewerWindow(NEWidget):

    def __init__(self, loading_manager: "LoadingManager", content, object: "LocationObject"):
        super().__init__()

        self.loading_manager = loading_manager
        self.content = content.content
        self.object = object

        pprint(self.content)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(3)
        #General title vs challenge title
        # name = content.get('localizedTextIdName') or content.get('localizedTextIdTitle') or content.get('localizedTextIdShort') or '- Unnamed -'
        # if '$' in name:
        #     name = link_referenced(loading_manager, name, False)
        # self.setWindowTitle(name)

        content_id = content.content_id

        if content_id == 0:
            display_datacube(self)

        elif content_id in [1, 6]:
            display_quest(self)

        elif content_id in [3, 5]:
            display_event(self)

        elif content_id == 4:
            display_challenge(self)

        elif content_id == 2:
            display_mission(self)

        else:
            raise TypeError('Cannot parse this data.')
        #Quest directions
        # PathMission, Quest, Challenge
        # test = data.get('questDirectionId') or data.get('questDirectionIdCompletion') or data.get('questDirectionIdActive')

        # if test:
        #     self.addQuestDirections(test, 1)

        self.setFixedWidth(WINDOW_WIDTH)
        #Add floating icons
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
    #             test = mapViewer.ObjectiveObject(objId)
    #             test.setPos(1, heightOffset)
    #             scene.addItem(test)
    #             objId += 1 

    #         heightOffset += widget.sizeHint().height() + 3
    
    def add_label(self, string_name: str):

        text = self.content.get(string_name)
        if text:
            self.main_layout.addWidget(ContentLabel(text, string_name))

    def showEvent(self, event: QShowEvent | None):
        #Focus on object
        if self.object:
            self.object.map_scene.focus(self.object)

        super().showEvent(event)

    def closeEvent(self, event: QCloseEvent | None):
        #Remove focus from object
        if self.object:
            self.object.map_scene.focus()

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
