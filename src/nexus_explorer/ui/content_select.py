
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .content_types import CONTENT_TYPES
from .content_viewer import ContentViewerWindow
from .widgets import HtmlDelegate

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
        #Level range
        min_level = content.get('preq_level') or content.get('minPlayerLevel')
        max_level = content.get('conLevel') or ''
        if min_level and int(min_level) > 0:
            name_list.append(f'<b>[lvl {min_level}-{max_level}]</b>')
        # Faction
        for key in content:
            if key.endswith('FactionEnum'):
                name_list.insert(0, f'<b>[{['Exile', 'Dominion', 'Neutral'][int(content[key])]}]</b>')
                break

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
        self.tree.itemClicked.connect(self.select_content)

        self.populate_list()

        self.layout.addWidget(self.tree)

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

    def select_content(self, item):
        # If it's not a category header
        if item.childCount() == 0:
            #Focus on icon
            self.icon.parent.focus(self.icon)

            self.content_viewer = ContentViewerWindow(self.loading_manager, item.content, self.icon)
            self.content_viewer.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.content_viewer.show()

    def closeEvent(self, event):
        #Remove focus from icon
        self.icon.setSelected(False)
        self.icon.parent.focus()
        
        super().closeEvent(event)
