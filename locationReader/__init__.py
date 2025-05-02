
from pprint import pprint

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from dataReader import challengeReader, datacubeReader, eventReader, questReader

from main import Settings

class ContentItem(QTreeWidgetItem):

    def __init__(self, data, dataType, *args, **kwargs):
        super(ContentItem, self).__init__(*args, **kwargs)

        self.data = data
        self.dataType = dataType

class Window(QWidget):

    def __init__(self, locData):
        super().__init__()

        self.setWindowTitle(locData['clusterName'])

        layout = QVBoxLayout()
        self.setLayout(layout)

        tree = QTreeWidget()
        tree.setHeaderHidden(True)

        categories = ['Challenge', 'Datacube', 'PublicEvent', 'PublicEventObjective', 'Quest2', 'QuestObjective']
        categoryNames = ['Challenges', 'Datacubes', 'Public Events', 'Public Event Objectives', 'Quests', 'Quest Objectives']
        
        iconPath = f"{Settings()['gameFiles']}/UI/Icon/"
        
        icons = ['Map/Node/UI_Map_Challenges/UI_Map_Challenges.png', 'Missions/Scientist_DatacubeDiscovery/Scientist_DatacubeDiscovery.png', 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'Map/Node/UI_Map_Quests/UI_Map_Quests.png']
        localizedTexts = ['localizedTextIdName', 'localizedTextIdTitle', 'localizedTextIdName', 'localizedTextIdShort', 'localizedTextIdTitle', 'localizedTextIdShort']

        for content in [content for content in sorted(locData) if content in categories]:

            index = categories.index(content)

            category = QTreeWidgetItem([categoryNames[index]])

            category.setIcon(0, QIcon(iconPath + icons[index]))

            categoryFont = QFont()
            categoryFont.setBold(True)
            category.setFont(0, categoryFont)

            for item in locData[content].values():

                if content == 'QuestObjective':

                    try:
                        category.addChild(ContentItem(item['Quest2'], content, [item[localizedTexts[index]]]))
                    
                    except:
                        pass

                elif content == 'PublicEventObjective':

                    try:
                        category.addChild(ContentItem(item['publicEventId'], content, [item[localizedTexts[index]]]))

                    except:
                        pass

                else:
                    category.addChild(ContentItem(item, content, [item[localizedTexts[index]]]))

            tree.addTopLevelItem(category)
            category.setExpanded(True)

        layout.addWidget(tree)
        tree.itemClicked.connect(self.popup)

        screen = QApplication.primaryScreen().geometry()
        self.setFixedSize(500, int(screen.height() / 2)) # - self.style().PixelMetric(QStyle.PM_TitleBarHeight)

        self.show()

    def popup(self, item):

        if item.dataType == 'Challenge':

            self.popup = challengeReader.window(item.data)

        elif item.dataType == 'Datacube':

            self.popup = datacubeReader.window(item.data)

        elif item.dataType == 'PublicEvent' or item.dataType == 'PublicEventObjective':

            self.popup = eventReader.window(item.data)

        elif item.dataType == 'Quest2' or item.dataType == 'QuestObjective':

            self.popup = questReader.window(item.data)
