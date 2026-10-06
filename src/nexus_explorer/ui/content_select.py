
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QStyle,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

from nexus_explorer.data.utilities import link_referenced

from .content_types import CONTENT_TYPES
from .content_viewer import ContentViewerWindow
from .extensions import HtmlDelegate, NEWidget

if TYPE_CHECKING:
    from nexus_explorer.data import LoadingManager

    from .map_viewer.objects import LocationObject, RegionObject

WINDOW_WIDTH = 400

class ContentCategory(QTreeWidgetItem):

    def __init__(self, content: list[dict], content_type: dict[str, int | str],  parent: QTreeWidget):
        super().__init__(parent)

        tree = self.treeWidget()
        if tree and tree.parent():
            loading_manager = tree.parent().loading_manager
        #Set category name and icon
        name = content_type['name']
        self.setText(0, name)
        self.setExpanded(True)

        categoryFont = QFont()
        categoryFont.setBold(True)
        self.setFont(0, categoryFont)

        self.setIcon(0, QIcon(f"{loading_manager.game_files}/UI/Icon/{content_type['icon']}"))
        #Add content under this category
        for item in content:
            self.addChild(ContentItem(loading_manager, item, content_type))

    def addChild(self, child):
        if child.text(0) not in [self.child(i).text(0) for i in range(self.childCount())]:
            super().addChild(child)

class ContentItem(QTreeWidgetItem):
    """Tree item that retains data"""
    def __init__(self, loading_manager: "LoadingManager", content: dict, content_type: dict):
        super().__init__()

        self.loading_manager = loading_manager
        self.content = content
        self.content_id = content_type['id']

        self.setText(0, self.get_name())

    def get_name(self) -> str:
        
        name_list = []
        #Name
        name = self.content.get('localizedTextIdName') or self.content.get('localizedTextIdTitle') or self.content.get('localizedTextIdShort') or '- Unnamed -'
        #Display referenced object
        if '$' in name:
            name = link_referenced(self.loading_manager, name)
            
        name_list.append(name)
        #Level range
        min_level = self.content.get('preq_level') or self.content.get('minPlayerLevel')
        max_level = self.content.get('conLevel') or ''
        if min_level and min_level > 0:
            name_list.append(f'<b>[lvl {min_level}-{max_level}]</b>')
        # Faction
        for key in self.content:
            if key.endswith('FactionEnum'):
                name_list.insert(0, f'<b>[{['Exile', 'Dominion', 'Neutral'][self.content[key]]}]</b>')
                break

        return ' '.join(name_list)

class ContentSelectWindow(NEWidget):
    """Categorize the content into their different types"""
    def __init__(self, loading_manager: "LoadingManager", object: "LocationObject | RegionObject"):
        super().__init__()

        self.loading_manager = loading_manager
        self.object = object

        self.setWindowIcon(QIcon(self.object._pixmap))
        self.setWindowTitle(self.object.name)

        screen = QApplication.primaryScreen()
        style = self.style()
        if screen and style:
            geometry = screen.availableGeometry()
            self.setFixedSize(WINDOW_WIDTH, geometry.height() - style.pixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
            self.move(geometry.right() - WINDOW_WIDTH, geometry.y())

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        # Add Tree
        self.tree = QTreeWidget(self)
        self.tree.setItemDelegate(HtmlDelegate(self.tree))
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.select_content)
        self.main_layout.addWidget(self.tree)

        self.populate_list()

    def add_category(self, content_id: int, content_data: list[dict]):
        #Path missions
        if content_id == 2:
            #One category per path
            for type_id in {mission['pathTypeEnum'] for mission in content_data}:
                self.tree.addTopLevelItem(
                    ContentCategory([mission for mission in content_data if mission['pathTypeEnum'] == type_id], CONTENT_TYPES[content_id][type_id], self.tree)
                )
        #Everything else
        else:
            self.tree.addTopLevelItem(
                ContentCategory(content_data, CONTENT_TYPES[content_id], self.tree)
            )

    def populate_list(self):

        for content_id, content_name in enumerate([
            'Datacube',
            'Quest2',
            'PathMission',
            'PublicEvent',
            'Challenge',
            'PublicEventObjective',
            'QuestObjective',
        ]):
            content_data = self.object.contents.get(content_name)
            if content_data:
                self.add_category(content_id, content_data)

    def select_content(self, item: ContentItem):
        #If it's not a category header
        if item.childCount() == 0:
            #Focus on object
            self.object.map_scene.focus(self.object)

            self.popup = ContentViewerWindow(self.loading_manager, item, self.object)
            self.popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.popup.show()

    def closeEvent(self, event: QCloseEvent | None):
        #Remove focus from object
        self.object.setSelected(False)
        self.object.map_scene.focus()

        super().closeEvent(event)
