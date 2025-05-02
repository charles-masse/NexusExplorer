
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QScreen
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QStyle, QApplication

from dataReader import challengeReader, datacubeReader, eventReader, questReader

from main import Settings

WINDOW_WIDTH = 450

CONTENT_TYPES = {
                 'Challenge' : {'name': 'Challenges', 'icon': 'Map/Node/UI_Map_Challenges/UI_Map_Challenges.png', 'text': 'localizedTextIdName'},
                 'Datacube' : {'name': 'Datacubes', 'icon': 'Missions/Scientist_DatacubeDiscovery/Scientist_DatacubeDiscovery.png', 'text': 'localizedTextIdTitle'},
                 'PublicEvent' : {'name': 'Public Events', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdName'},
                 'PublicEventObjective' : {'name': 'Public Event Objectives', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdShort'},
                 'Quest2' : {'name': 'Quests', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdTitle'},
                 'QuestObjective' : {'name': 'Quest Objectives', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdShort'}
                }

class ContentItem(QTreeWidgetItem):
    """
    Tree item that retains data
    """
    def __init__(self, data, dataType, *args, **kwargs):
        super(ContentItem, self).__init__(*args, **kwargs)

        self.dataType = dataType
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
        tree.setHeaderHidden(True)
        layout.addWidget(tree)
        tree.itemClicked.connect(self.popup)

        for content in [content for content in locData if content in CONTENT_TYPES.keys()]:
            # Add section header
            category = QTreeWidgetItem([CONTENT_TYPES[content]['name']])
            category.setIcon(0, QIcon(f"{Settings()['gameFiles']}/UI/Icon/{CONTENT_TYPES[content]['icon']}"))
            category.setExpanded(True)

            categoryFont = QFont()
            categoryFont.setBold(True)
            category.setFont(0, categoryFont)

            tree.addTopLevelItem(category)
            # Add content
            for item in locData[content].values():

                if content == 'QuestObjective':

                    try:
                        category.addChild(ContentItem(item['Quest2'], content, [item[CONTENT_TYPES[content]['text']]]))
                    
                    except:
                        pass

                elif content == 'PublicEventObjective':

                    try:
                        category.addChild(ContentItem(item['publicEventId'], content, [item[CONTENT_TYPES[content]['text']]]))

                    except:
                        pass

                else:
                    category.addChild(ContentItem(item, content, [item[CONTENT_TYPES[content]['text']]]))

        self.show()

    def popup(self, item):
        """
        This needs to change
        """
        try:
            if item.dataType == 'Challenge':
                challengeReader.window(item.data)

            elif item.dataType == 'Datacube':
                datacubeReader.window(item.data)

            elif item.dataType == 'PublicEvent' or item.dataType == 'PublicEventObjective':
                eventReader.window(item.data)

            elif item.dataType == 'Quest2' or item.dataType == 'QuestObjective':
                questReader.window(item.data)

        except:
            pass
