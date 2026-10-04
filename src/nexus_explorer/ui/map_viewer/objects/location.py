
from typing import TYPE_CHECKING

from PyQt6.QtCore import QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QPen, QPixmap
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsObject, QStyle

from ...content_types import CONTENT_TYPES
from ..utilities import world_to_screen_pos

if TYPE_CHECKING:
    from ..window import MapScene

ICON_SIZE = 32

class LocationObject(QGraphicsObject):
    """An icon on the map that retains data and has a glow effect"""
    clicked = pyqtSignal(QGraphicsObject)

    def __init__(self, data, map_scene: "MapScene"):
        super().__init__()

        self.name = data._get_name() or 'Untitled Location'
        self.contents = data.contents
        self.map_scene = map_scene
        #Make it selectable
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self._pen = QPen(QColor(255, 255, 0, 180), 6)
        #Show icon
        self._pixmap = QPixmap(f"{map_scene.loading_manager.game_files}/UI/Icon/{self.get_icon()}").scaled(ICON_SIZE, ICON_SIZE)
        #Set position
        pos = data.get_position()
        screen_x, screen_y = world_to_screen_pos(pos[0], pos[1])
        self.setPos(screen_x - (ICON_SIZE / 2), screen_y - (ICON_SIZE / 2))
        self.setZValue(1)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._pixmap.width(), self._pixmap.height())

    def get_icon(self) -> str | None:
        #Go through all icons by priority
        for content_id, content in enumerate(
            [
                self.contents.get('QuestHub', []),
                self.contents.get('Datacube', []),
                self.contents.get('Quest2', []),
                self.contents.get('PathMission', []),
                self.contents.get('PublicEvent', []),
                self.contents.get('Challenge', [])
            ]
        ):

            if len(content):
                #Faction hubs
                if content_id == 0:

                    faction_icons = [
                        'Map/Node/Map_QuestHub_Exile/Map_QuestHub_Exile.png',
                        'Map/Node/Map_QuestHub_Dominion/Map_QuestHub_Dominion.png',
                        'Map/Node/Map_QuestHub/Map_QuestHub.png'
                    ]

                    quest_factions = [quest['questPlayerFactionEnum'] for quest in self.contents.get('Quest2', [])]

                    if len(quest_factions):
                        faction_id = max(quest_factions, key=quest_factions.count)
                        icon = faction_icons[faction_id]

                    else:
                        icon = faction_icons[2]

                    break
                #Path Missions
                elif content_id == 3:

                    mission_types = [mission['pathTypeEnum'] for mission in content]
                    mission_id = max(mission_types, key=mission_types.count)

                    icon = CONTENT_TYPES[content_id - 1][mission_id]['icon']

                    break

                else:
                    icon = CONTENT_TYPES[content_id - 1]['icon']

                    break

        else:
            icon = "Map/Node/Map_NavPoint/Map_NavPoint.png"

        return icon

    def paint(self, painter, option, widget=None):
        
        painter.setPen(self._pen)

        if self.isSelected():
            painter.drawEllipse(self.boundingRect().adjusted(3, 3, -3, -3))
        #Remove selection box
        painter.drawPixmap(0, 0, self._pixmap)

        option.state &= ~QStyle.StateFlag.State_Selected

    def mousePressEvent(self, event):

        self.map_scene.select_object(self)

        super().mousePressEvent(event)
