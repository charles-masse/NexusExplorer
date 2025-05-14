
from PyQt6.QtGui import QIcon, QFont, QScreen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from ui import HtmlDelegate
from windows import contentReader
from singletons import settings, LocalizedStrings, loadManager
from actions.links import linkGameObject

WINDOW_WIDTH = 400

CONTENT_TYPES = {
                 'Datacube' : {'name': 'Datacubes', 'icon': '/Map/Node/UI_Map_Scientist/UI_Map_Scientist.png', 'text': 'localizedTextIdTitle'},
                 'Quest2' : {'name': 'Quests', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdTitle'},
                 'QuestObjective' : {'name': 'Quest Objectives', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdShort'},
                 'PublicEvent' : {'name': 'Public Events', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdName'},
                 'PublicEventObjective' : {'name': 'Public Event Objectives', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdShort'},
                 'Challenge' : {'name': 'Challenges', 'icon': 'Map/Node/UI_Map_Challenges/UI_Map_Challenges.png', 'text': 'localizedTextIdName'},
                }

class ContentItem(QTreeWidgetItem):
    """
    Tree item that retains data
    """
    def __init__(self, data, *args, **kwargs): # dataType,
        super(ContentItem, self).__init__(*args, **kwargs)

        self.data = data

class Window(QWidget):
    """
    Categorize the content into their different types
    """
    def __init__(self, locData):
        super().__init__()

        self.setWindowTitle(locData['clusterName'])

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(WINDOW_WIDTH, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.getRect()[0] + screen.getRect()[2] - WINDOW_WIDTH, screen.y())

        layout = QVBoxLayout()
        self.setLayout(layout)
        # Add Tree
        tree = QTreeWidget()
        self.delegate = HtmlDelegate(tree)
        tree.setItemDelegate(self.delegate)
        tree.setHeaderHidden(True)
        tree.itemClicked.connect(self.popup)

        for contentType in [ct for ct in CONTENT_TYPES if ct in locData]:
            # Add section header
            categoryName = CONTENT_TYPES[contentType]['name']
            category = QTreeWidgetItem([categoryName])
            category.setIcon(0, QIcon(f"{settings['gameFiles']}/UI/Icon/{CONTENT_TYPES[contentType]['icon']}"))

            categoryFont = QFont()
            categoryFont.setBold(True)
            category.setFont(0, categoryFont)

            tree.addTopLevelItem(category)
            category.setExpanded(True)
            # Add content
            for content in locData[contentType].values():

                name = LocalizedStrings[content[CONTENT_TYPES[contentType]['text']]]

                if not name:
                    name = '[Unnamed]'

                if '$' in name:
                    name = linkGameObject(name)

                # Quest faction
                faction = content.get('questPlayerFactionEnum')
                if faction:
                    name = ' '.join([f'<b>[{['Exile', 'Dominion', 'Neutral'][int(faction)]}]</b>', name])

                if contentType == 'QuestObjective':
                    content = loadManager['Quest2'].get(content['Quest2'], {})

                elif contentType == 'PublicEventObjective':
                    content = loadManager['PublicEvent'].get(content['publicEventId'], {})

                category.addChild(ContentItem(content, [name]))

        layout.addWidget(tree)

    def popup(self, item):

        self.popup = contentReader.Window(item.data)
        self.popup.show()
