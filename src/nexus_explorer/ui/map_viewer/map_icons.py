
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ..content_types import CONTENT_TYPES
from .utilities import world_to_screen_pos

ICON_SIZE = 32

class LocationObject(QGraphicsObject):
    """An icon on the map that retains data, sends signals and has a glow effect
    """
    clicked = pyqtSignal(QGraphicsObject)

    def __init__(self, location, parent=None):
        super().__init__()

        self.location = location

        self.pixmap = QPixmap(f'{parent.loading_manager.game_files}/UI/Icon/{self.get_icon()}').scaled(ICON_SIZE, ICON_SIZE)

        screen_x, screen_y = world_to_screen_pos(*self.location.position)
        self.setPos(screen_x - (ICON_SIZE / 2), screen_y - (ICON_SIZE / 2))

        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.pixmap.width(),
            self.pixmap.height()
        )

    def get_icon(self):
        #Go through all icons by priority
        for content_id, content in enumerate(
            [
                self.location.hubs,
                self.location.datacubes,
                self.location.quests,
                self.location.missions,
                self.location.events,
                self.location.challenges
            ]
        ):
                    
            if len(content):
                # Faction hubs
                if content_id == 0:

                    faction_icons = [
                        'Map/Node/Map_QuestHub_Exile/Map_QuestHub_Exile.png',
                        'Map/Node/Map_QuestHub_Dominion/Map_QuestHub_Dominion.png',
                        'Map/Node/Map_QuestHub/Map_QuestHub.png'
                    ]
                            
                    quest_factions = [int(quest['questPlayerFactionEnum']) for quest in self.location.quests]

                    if len(quest_factions):

                        test = max(quest_factions, key=quest_factions.count)
                        icon = faction_icons[test]

                    else:
                        icon = faction_icons[2]

                    break
                # Path Missions
                elif content_id == 3:

                    mission_types = [int(mission['pathTypeEnum']) for mission in content]
                    mission_id = max(mission_types, key=mission_types.count)

                    icon = CONTENT_TYPES[content_id - 1][mission_id]['icon']

                    break

                else:
                    icon = CONTENT_TYPES[content_id - 1]['icon']

                    break

        else:
            icon = 'Map/Node/Map_NavPoint/Map_NavPoint.png'

        return icon

    def paint(self, painter, option, widget=None):

        if self.isSelected():
            pen = QPen(QColor(255, 255, 0, 180), 6)
            painter.setPen(pen)
            painter.drawEllipse(self.boundingRect().adjusted(3, 3, -3, -3))
        # Remove selection box
        painter.drawPixmap(0, 0, self.pixmap)

        option.state &= ~QStyle.StateFlag.State_Selected

    def mouseReleaseEvent(self, event):
        self.clicked.emit(self)
        super().mouseReleaseEvent(event)

# class ObjectiveIcon(QGraphicsPixmapItem):

#     def __init__(self, objectiveId):
#         super().__init__()

#         self.pixmap = QPixmap(f'{settings['gameFiles']}/UI/Assets/TexPieces/UI_CRB_HUD_Tracker_349_73/UI_CRB_HUD_Tracker_349_73.png')
#         self.setPixmap(self.pixmap)

#         self.text = QGraphicsTextItem(str(objectiveId), self)
#         self.text.setDefaultTextColor(QColor('white'))
#         self.text.setFont(QFont(f'{settings['gameFiles']}/UI/Fonts/segoeuib.ttf', 10))

#         textRect = self.text.boundingRect()
#         self.text.setPos((self.pixmap.width() / 2) - (textRect.width() / 2), 0)
