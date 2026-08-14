
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .content_types import CONTENT_TYPES
from .widgets import HtmlDelegate

# from src.windows import contentReader

WINDOW_WIDTH = 400

class ContentCategory(QTreeWidgetItem):

    def __init__(self, content, content_dict, tree):
        super().__init__(tree)

        name = content_dict['name']
        icon = f"{tree.parent().loading_manager.game_files}/UI/Icon/{content_dict['icon']}"

        self.setText(0, name)
        self.setIcon(0, QIcon(icon))

        categoryFont = QFont()
        categoryFont.setBold(True)
        self.setFont(0, categoryFont)
        #Add content
        for item in content:
            self.addChild(ContentItem(item, self))

class ContentItem(QTreeWidgetItem):
    """Tree item that retains data
    """
    def __init__(self, content, parent):
        super().__init__(parent, [self.get_name(content)])

        self.content = content

    def get_name(self, content):
        name_list = []
        #Name
        #TODO linked objects with $
        name_list.append(content.get('name') or content.get('title') or content.get('short') or '- Unnamed -')
        #Level
        level = content.get('preq_level')
        if level != None:
            name_list.append(f'<b>[lvl {level}]</b>')
        # Faction
        faction_id = content.get('questPlayerFactionEnum') or content.get('pathMissionFactionEnum')
        if faction_id != None:
            name_list.insert(0, f'<b>[{['Exile', 'Dominion', 'Neutral'][int(faction_id)]}]</b>')

        return ' '.join(name_list)

class ContentSelectWindow(QWidget):
    """Categorize the content into their different types
    """
    def __init__(self, loading_manager, icon):
        super().__init__()

        self.loading_manager = loading_manager
        self.icon = icon

        self.setWindowTitle(self.icon.location.name or 'Untitled Location')
        self.setWindowIcon(QIcon(self.icon.pixmap))

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(WINDOW_WIDTH, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.getRect()[0] + screen.getRect()[2] - WINDOW_WIDTH, screen.y())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Add Tree
        self.tree = QTreeWidget(self)
        self.tree.setItemDelegate(HtmlDelegate(self.tree))
        self.tree.setHeaderHidden(True)
        # self.tree.itemClicked.connect(self.popup) #TODO

        self.populate_list()

        self.layout.addWidget(self.tree)

        # self.mapView.focusOn()

    def add_category(self, content, content_dict):
        category = ContentCategory(content, content_dict, self.tree)
        self.tree.addTopLevelItem(category)
        category.setExpanded(True)

    def populate_list(self):

        location = self.icon.location
        
        for content_id, content in enumerate(
            [
                location.datacubes,
                location.quests,
                location.missions,
                location.events,
                location.challenges
            ]
        ):

            if len(content):
                # Path Missions
                if content_id == 2:
                    # Create a category for each mission type
                    for type_id in {int(mission['pathTypeEnum']) for mission in content}:
                        self.add_category(content, CONTENT_TYPES[content_id][type_id])

                else:
                    self.add_category(content, CONTENT_TYPES[content_id])

    # def popup(self, item):
    #     # If it's not a category header
    #     if item.childCount() == 0:

    #         self.mapView.focusOn(self.locIcon)

    #         self.popup = contentReader.Window(item.data, self.mapView)
    #         self.popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    #         self.popup.show()

    # def closeEvent(self, event):
    #     self.locIcon.setSelected(False)
    #     self.popup.close()
