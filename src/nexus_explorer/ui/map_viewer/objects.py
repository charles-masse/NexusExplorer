
from typing import TYPE_CHECKING

from PyQt6.QtCore import QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPen, QPixmap
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
    QStyle,
)

from ...data import LocationData
from ..content_types import CONTENT_TYPES
from .utilities import world_to_screen_pos

if TYPE_CHECKING:
    from .map_viewer import MapScene

ICON_SIZE = 32

class LocationObject(QGraphicsObject):
    """An icon on the map that retains data, sends signals and has a glow effect"""
    clicked = pyqtSignal(QGraphicsObject)

    def __init__(self, location: LocationData, map_scene: "MapScene"):
        super().__init__()

        self.location = location
        self.map_scene = map_scene

        self._pen = QPen(QColor(255, 255, 0, 180), 6)
        
        self.pixmap = QPixmap(f'{self.map_scene.loading_manager.game_files}/UI/Icon/{self.get_icon()}').scaled(ICON_SIZE, ICON_SIZE)

        screen_x, screen_y = world_to_screen_pos(*self.location.position)
        self.setPos(screen_x - (ICON_SIZE / 2), screen_y - (ICON_SIZE / 2))

        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def boundingRect(self) -> QRectF:
        return QRectF(
            0,
            0,
            self.pixmap.width(),
            self.pixmap.height()
        )

    def get_icon(self) -> str | None:
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
                            
                    quest_factions = [quest['questPlayerFactionEnum'] for quest in self.location.quests]

                    if len(quest_factions):
                        faction_id = max(quest_factions, key=quest_factions.count)
                        icon = faction_icons[faction_id]

                    else:
                        icon = faction_icons[2]

                    break
                # Path Missions
                elif content_id == 3:

                    mission_types = [mission['pathTypeEnum'] for mission in content]
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

        painter.setPen(self._pen)

        if self.isSelected():
            painter.drawEllipse(self.boundingRect().adjusted(3, 3, -3, -3))
        # Remove selection box
        painter.drawPixmap(0, 0, self.pixmap)

        option.state &= ~QStyle.StateFlag.State_Selected

    def mouseReleaseEvent(self, event):
        self.clicked.emit(self)
        super().mouseReleaseEvent(event)

class ObjectiveObject(QGraphicsPixmapItem):

    def __init__(self, objectiveId: int, game_files: str):
        super().__init__()

        self.im = QPixmap(f'{game_files}/UI/Assets/TexPieces/UI_CRB_HUD_Tracker_349_73/UI_CRB_HUD_Tracker_349_73.png')
        self.setPixmap(self.im)

        self.text = QGraphicsTextItem(str(objectiveId), self)
        self.text.setDefaultTextColor(QColor('white'))
        self.text.setFont(QFont(f'{game_files}/UI/Fonts/segoeuib.ttf', 10))

        textRect = self.text.boundingRect()
        self.text.setPos((self.im.width() / 2) - (textRect.width() / 2), 0)

class RegionObject(QGraphicsObject):
    clicked = pyqtSignal()

    def __init__(self, polygon, parent=None):
        super().__init__(parent)

        self._polygon = polygon
        self._pen = QPen(QColor("black"), 2)

    def boundingRect(self):
        pad = self._pen.widthF() / 2.0
        return self._polygon.boundingRect().adjusted(-pad, -pad, pad, pad)

    def paint(self, painter, option, widget=None):
        """Draws the actual polygon on the scene."""
        painter.setPen(self._pen)
        painter.drawPolygon(self._polygon)

    # def mousePressEvent(self, event):
    #     self.clicked.emit()
    #     super().mousePressEvent(event)
