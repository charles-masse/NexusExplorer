
import re

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from windows import contentReader

from singletons import settings, localizedStrings, creatures, items

from pprint import pprint

WINDOW_WIDTH = 600

CONTENT_TYPES = {
                 'Challenge' : {'name': 'Challenges', 'icon': 'Map/Node/UI_Map_Challenges/UI_Map_Challenges.png', 'text': 'localizedTextIdName'},
                 'Datacube' : {'name': 'Datacubes', 'icon': 'Missions/Scientist_DatacubeDiscovery/Scientist_DatacubeDiscovery.png', 'text': 'localizedTextIdTitle'},
                 'PublicEvent' : {'name': 'Public Events', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdName'},
                 'PublicEventObjective' : {'name': 'Public Event Objectives', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdShort'},
                 'Quest2' : {'name': 'Quests', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdTitle'},
                 'QuestObjective' : {'name': 'Quest Objectives', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdShort'}
                }

def paleFire(text):

    matches = re.finditer(r'(?:<text[^>]*?>)?\$(?:\w*\((\w+)=(\d+)\)|(\w+)=(\d+))(?:</text>)?', text)
    
    for match in matches:

        fullMath = match.group(0)
        key = match.group(1) or match.group(3)
        idValue = match.group(2) or match.group(4)

        if key == 'creature':
            text = text.replace(fullMath, f'<b>[{localizedStrings[creatures[idValue].get('localizedTextIdName', '')]}]</b>')

        elif key == 'vitem':
            text = text.replace(fullMath, f'<b>[{localizedStrings[items[idValue].get('localizedTextIdName', '')]}]</b>')

        else:
            text = text.replace(fullMath, f'<b>[{key}:{idValue}]</b>')

    return text

class ContentItem(QTreeWidgetItem):
    """
    Tree item that retains data
    """
    def __init__(self, data, dataType, *args, **kwargs):
        super(ContentItem, self).__init__(*args, **kwargs)

        self.data = data
        self.dataType = dataType

class HtmlDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):

        painter.save()
        painter.setClipRect(option.rect)
        # Skip category header to retain icons
        if not index.parent().isValid():
            super().paint(painter, option, index)
            return

        doc = QTextDocument()
        doc.setDefaultFont(option.font)
        doc.setHtml(index.data())
        doc.setTextWidth(option.rect.width())
        doc.setDocumentMargin(0)

        context = doc.documentLayout().PaintContext()
        context.palette.setColor(QPalette.ColorRole.Text, QColor(125, 251, 182))

        if option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, QColor(0, 100, 180, 50))

        painter.translate(option.rect.topLeft())
        
        doc.documentLayout().draw(painter, context)

        painter.restore()

    def sizeHint(self, option, index):

        doc = QTextDocument()
        doc.setDefaultFont(option.font)
        doc.setHtml(index.data())
        doc.setTextWidth(option.rect.width())
        doc.setDocumentMargin(0)

        return doc.size().toSize()

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
                # Replace game object link
                if name and '$' in name:
                    name = paleFire(name)

                elif not name:
                    name = '<b>[Unnamed]</b>'
                # Get parent for objectives--might go away at some point
                if contentType == 'QuestObjective':
                    content = location.get('Quest2', {})
                    
                elif contentType == 'PublicEventObjective':
                    content = location.get('publicEventId', {})

                else:
                    content = location

                category.addChild(ContentItem(content, contentType, [name])) 

        layout.addWidget(tree)

    def popup(self, item):

        # contentReader.Window(item.data)
        print(item.data)
