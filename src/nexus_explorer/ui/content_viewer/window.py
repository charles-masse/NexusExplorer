
from pprint import pprint
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QShowEvent
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QVBoxLayout,
)

from nexus_explorer.data.utilities import link_referenced
from nexus_explorer.ui.content_viewer.labels import ContentLabel
from nexus_explorer.ui.extensions import NEWidget
from nexus_explorer.ui.map_viewer.objects import ObjectiveObject, RegionObject

from .types import (
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

    def __init__(self, loading_manager: "LoadingManager", content, map_object: "LocationObject"):
        super().__init__()

        pprint(content.content)

        self.loading_manager = loading_manager
        self.content = content.content
        self.map_object = map_object

        self.cleanup: list[ObjectiveObject | RegionObject] = []
        #General title vs challenge title
        name = self.content.get('localizedTextIdName') or self.content.get('localizedTextIdTitle') or self.content.get('localizedTextIdShort') or '- Unnamed -'
        if '$' in name:
            name = link_referenced(loading_manager, name, False)
        self.setWindowTitle(name)

        self.main_layout = QHBoxLayout(self)

        self.right_layout = QVBoxLayout()
        self.right_layout.setSpacing(3)
        self.main_layout.addLayout(self.right_layout)

        content_id = content.content_id

        if content_id == 0:
            display_datacube(self)

        elif content_id in [1]: # , 6
            display_quest(self)

        elif content_id == 2:
            display_mission(self)

        elif content_id in [3]: # , 5
            display_event(self)

        elif content_id == 4:
            display_challenge(self)

        else:
            raise TypeError('Cannot parse this data.')
        #Resize
        self.setMinimumWidth(WINDOW_WIDTH)
        #Floating numbers
        view = QGraphicsView(self)
        view.setStyleSheet("background: transparent; border: 0;")
        view.setFixedSize(WINDOW_WIDTH, self.sizeHint().height())
        view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, view.width(), view.height())
        view.setScene(scene)

        objective_id = 1
        heightOffset = 0
        #Go through all the labels
        for i in range(self.right_layout.count()):
            item = self.right_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    #If label is an objective
                    if widget.objectName() == 'LabelObjective':

                        objective = ObjectiveObject(str(objective_id), [0,0])
                        objective.setPos(1, heightOffset)
                        scene.addItem(objective)

                        objective_id += 1
                    #Save the size of the widget
                    heightOffset += widget.sizeHint().height() + 3

    def add_label(self, text: str, type: str):
        if text:
            #TODO
            if type == 'LabelSay':
                prefix = '> '
            else:
                prefix = ''

            self.right_layout.addWidget(ContentLabel(link_referenced(self.loading_manager, prefix + text), type))

    def add_map_location(self, loc, text):
        #Add icon #TODO make sure the icon is on the same map
        obj = self.map_object.map_scene.draw_objective((loc['position0'], loc['position2']), text)
        self.cleanup.append(obj)
        #Reveal map zone
        for map_object in self.map_object.map_scene.items():
            if isinstance(map_object, RegionObject) and loc['worldZoneId'] == map_object.contents['MapZone'][0]['worldZoneId']:
                map_object.show()
                map_object.display_override = True
                map_object.update()
                self.cleanup.append(map_object)
                break

    def showEvent(self, event: QShowEvent | None):
        super().showEvent(event)

        screen = QApplication.primaryScreen()
        if screen:
            frame_geometry = self.frameGeometry()
            frame_geometry.moveCenter(screen.availableGeometry().center())
            self.move(frame_geometry.topLeft())
        #Focus on object
        if self.map_object:
            self.map_object.map_scene.focus(self.map_object)

    def closeEvent(self, event: QCloseEvent | None):

        scene = self.map_object.map_scene
        #Remove map objects that were created by this window
        for obj in self.cleanup:
            if isinstance(obj, RegionObject):
                #Hide the region
                if obj.contents["MapZone"][0]["mapZoneIdParent"] and not obj.contents.get('WorldLocation2'):
                    obj.hide()
                
                obj.display_override = False
                obj.update()

            else:
                scene.removeItem(obj)
        #Remove focus from object
        if self.map_object:
            scene.focus()

        super().closeEvent(event)
