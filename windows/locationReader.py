
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ui import HtmlDelegate
from windows import contentReader
from singletons import settings, LocalizedStrings, loadManager
from actions.links import linkGameObject

WINDOW_WIDTH = 400

CONTENT_TYPES = {
                 'QuestHub' : {'icon': [
                                        'Map/Node/Map_QuestHub_Exile/Map_QuestHub_Exile.png',
                                        'Map/Node/Map_QuestHub_Dominion/Map_QuestHub_Dominion.png',
                                        'Map/Node/Map_QuestHub/Map_QuestHub.png'
                                       ]
                              },
                 'Datacube' : {'name': 'Datacubes', 'icon': 'Missions/Scientist_DatacubeDiscovery/Scientist_DatacubeDiscovery.png', 'text': 'localizedTextIdTitle'},
                 'Quest2' : {'name': 'Quests', 'icon': 'Map/Node/UI_Map_Quests/UI_Map_Quests.png', 'text': 'localizedTextIdTitle'},
                 'PathMission' : {'name': [
                                           'Solider Mission',
                                           'Settler Mission',
                                           'Scientist Mission',
                                           'Explorer Mission'
                                          ], 
                                  'icon': [
                                           'Map/Node/UI_Map_Soldier/UI_Map_Soldier.png',
                                           'Map/Node/UI_Map_Settler/UI_Map_Settler.png',
                                           'Map/Node/UI_Map_Scientist/UI_Map_Scientist.png',
                                           'Map/Node/UI_Map_Explorer/UI_Map_Explorer.png'
                                          ],
                                  'text': 'localizedTextIdName'
                                 },
                 'PublicEvent' : {'name': 'Public Events', 'icon': 'Map/Node/UI_Map_Events/UI_Map_Events.png', 'text': 'localizedTextIdName'},
                 'Challenge' : {'name': 'Challenges', 'icon': 'Map/Node/UI_Map_Challenges/UI_Map_Challenges.png', 'text': 'localizedTextIdName'},
                 'QuestObjective' : {'name': 'Quest Objectives', 'icon': 'Map/Node/Map_NavPoint/Map_NavPoint.png', 'text': 'localizedTextIdShort'},
                 'PublicEventObjective' : {'name': 'Public Event Objectives', 'icon': 'Map/Node/Map_NavPoint/Map_NavPoint.png', 'text': 'localizedTextIdShort'}
                }

class ContentCategory(QTreeWidgetItem):

    def __init__(self, contents, contentType, typeId=None, *args, **kwargs):
        super(ContentCategory, self).__init__(*args, **kwargs)

        if typeId == None:
            name = CONTENT_TYPES[contentType]['name']
            icon = f"{settings['gameFiles']}/UI/Icon/{CONTENT_TYPES[contentType]['icon']}"

        else:   
            name = CONTENT_TYPES[contentType]['name'][typeId]
            icon = f"{settings['gameFiles']}/UI/Icon/{CONTENT_TYPES[contentType]['icon'][typeId]}"

        self.setText(0, name)
        self.setIcon(0, QIcon(icon))

        categoryFont = QFont()
        categoryFont.setBold(True)
        self.setFont(0, categoryFont)
        # Add content
        for content in contents[contentType].values():
            if typeId == None or typeId == int(content['pathTypeEnum']):

                childName = LocalizedStrings[content[CONTENT_TYPES[contentType]['text']]]

                if not childName:
                    childName = '-Unnamed-'

                if '$' in childName:
                    childName = linkGameObject(childName)
                # Level
                level = content.get('preq_level')

                if level:
                    childName += f' <b>[lvl {level}]</b>'
                # Faction
                faction = content.get('questPlayerFactionEnum') or content.get('pathMissionFactionEnum')
                if faction and contentType == 'Quest2':
                    childName = ' '.join([f'<b>[{['Exile', 'Dominion', 'Neutral'][int(faction)]}]</b>', childName])

                self.addChild(ContentItem(content, [childName]))

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
    def __init__(self, mapView, locIcon):
        super().__init__()

        self.mapView = mapView
        self.locIcon = locIcon

        self.setWindowTitle(locIcon.parent.content['clusterName'])
        self.setWindowIcon(QIcon(locIcon.pixmap()))

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(WINDOW_WIDTH, screen.height() - self.style().PixelMetric(QStyle.PixelMetric.PM_TitleBarHeight))
        self.move(screen.getRect()[0] + screen.getRect()[2] - WINDOW_WIDTH, screen.y())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Add Tree
        self.tree = QTreeWidget()
        self.delegate = HtmlDelegate(self.tree)
        self.tree.setItemDelegate(self.delegate)
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.popup)

        for contentType in [ct for ct in CONTENT_TYPES if ct in locIcon.parent.content if ct != 'QuestHub']:

            if contentType == 'PathMission':

                for typeId in set(tid['pathTypeEnum'] for tid in locIcon.parent.content['PathMission'].values()):
                    category = ContentCategory(locIcon.parent.content, contentType, typeId=int(typeId))
                    self.tree.addTopLevelItem(category)
                    category.setExpanded(True)

            else:
                category = ContentCategory(locIcon.parent.content, contentType)
                self.tree.addTopLevelItem(category)
                category.setExpanded(True)

        self.layout.addWidget(self.tree)

        self.mapView.focusOn()

    def popup(self, item):
        # If it's not a category header
        if item.childCount() == 0:

            self.mapView.focusOn(self.locIcon)

            self.popup = contentReader.Window(item.data, self.mapView)
            self.popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.popup.show()

    def closeEvent(self, event):

        self.locIcon.setSelected(False)
        try:
            self.popup.close()

        except:
            pass
