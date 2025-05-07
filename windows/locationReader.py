
import re

from PyQt6.QtGui import QIcon, QFont, QScreen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from ui import HtmlDelegate
from windows import contentReader
from singletons import settings, localizedStrings, creatures, items

WINDOW_WIDTH = 600

CONTENT_TYPES = {
                 'Challenge' : {'name': 'Challenges', 'icon': 'Map/Node/UI_Map_Challenges/UI_Map_Challenges.png', 'text': 'localizedTextIdName'},
                 'Datacube' : {'name': 'Datacubes', 'icon': 'Missions/Scientist_DatacubeDiscovery/Scientist_DatacubeDiscovery.png', 'text': 'localizedTextIdTitle'},
                 'PublicEvent' : {'name': 'Public Events', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdName'},
                 # 'PublicEventObjective' : {'name': 'Public Event Objectives', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdShort'},
                 'Quest2' : {'name': 'Quests', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdTitle'},
                 # 'QuestObjective' : {'name': 'Quest Objectives', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdShort'}
                }

def paleFire(text):
    """
    Change me please
    """
    matches = re.finditer(r'(?:<text[^>]*?>)?\$(?:\w*\((\w+)=(\d+)\)|(\w+)=(\d+))(?:</text>)?', text)
    
    for match in matches:

        fullMath = match.group(0)
        key = match.group(1) or match.group(3)
        idValue = match.group(2) or match.group(4)

        if key.lower() == 'creature':
            text = text.replace(fullMath, f'<b>[{localizedStrings[creatures[idValue].get('localizedTextIdName', "Can't find creature")]}]</b>')

        elif key.lower() == 'vitem':
            text = text.replace(fullMath, f'<b>[{localizedStrings[items[idValue].get('localizedTextIdName', "Can't find item")]}]</b>')

        else:
            text = text.replace(fullMath, f'<b>[{key}:{idValue}]</b>')

    return text

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

        for contentType in [c for c in locData if c in CONTENT_TYPES.keys()]:
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
            for location in locData[contentType].values():

                name = localizedStrings[location[CONTENT_TYPES[contentType]['text']]]

                if not name:
                    name = '<b>[Unnamed]</b>'
                # Replace game object link
                if '$' in name:
                    name = paleFire(name)

                category.addChild(ContentItem(location, [name]))

        layout.addWidget(tree)

    def popup(self, item):

        self.popup = contentReader.Window(item.data)
        self.popup.show()
