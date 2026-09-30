
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import QPointF, QRectF, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPen, QPixmap, QPolygonF
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
    QStyle,
)

from ..content_types import CONTENT_TYPES
from .utilities import hex_to_world_coordinates, world_to_screen_pos

if TYPE_CHECKING:
    from ...data.types import LocationData
    from .window import MapScene

ICON_SIZE = 32

class LocationObject(QGraphicsObject):
    """An icon on the map that retains data and has a glow effect"""
    clicked = pyqtSignal(QGraphicsObject)

    def __init__(self, content: "LocationData", map_scene: "MapScene"):
        super().__init__()

        self.content = content
        self.map_scene = map_scene

        self._pen = QPen(QColor(255, 255, 0, 180), 6)
        
        self.pixmap = QPixmap(f'{map_scene.loading_manager.game_files}/UI/Icon/{self.get_icon()}').scaled(ICON_SIZE, ICON_SIZE)

        screen_x, screen_y = world_to_screen_pos(*self.content.position)
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
                self.content.hubs,
                self.content.datacubes,
                self.content.quests,
                self.content.missions,
                self.content.events,
                self.content.challenges
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
                            
                    quest_factions = [quest['questPlayerFactionEnum'] for quest in self.content.quests]

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

    def mousePressEvent(self, event):

        self.map_scene.select_object(self)

        super().mousePressEvent(event)

class ObjectiveObject(QGraphicsPixmapItem):

    def __init__(self, objectiveId: int, game_files: str):
        super().__init__()

        im = QPixmap(f'{game_files}/UI/Assets/TexPieces/UI_CRB_HUD_Tracker_349_73/UI_CRB_HUD_Tracker_349_73.png')
        self.setPixmap(im)

        text = QGraphicsTextItem(str(objectiveId), self)
        text.setDefaultTextColor(QColor('white'))
        text.setFont(QFont(f'{game_files}/UI/Fonts/segoeuib.ttf', 10))

        textRect = text.boundingRect()
        text.setPos((im.width() / 2) - (textRect.width() / 2), 0)

class RegionObject(QGraphicsObject):

    def __init__(self, map_zone: dict, content: dict, map_scene: "MapScene"):
        super().__init__()

        self.map_zone = map_zone
        self.content = content
        self.map_scene = map_scene

        self.setAcceptHoverEvents(True)
        self.is_hovered = False
        self._pixmap = None
        self._pixmap_rect = QRectF()
        #Create polygon
        min_x, min_y = world_to_screen_pos(*hex_to_world_coordinates(map_zone['hexMinX'] - 1, map_zone['hexMinY'] - 0.5))
        max_x, max_y = world_to_screen_pos(*hex_to_world_coordinates(map_zone['hexLimX'] + 1, map_zone['hexLimY'] + 1))
        self._polygon = QPolygonF([QPointF(min_x, min_y), QPointF(max_x, min_y), QPointF(max_x, max_y), QPointF(min_x, max_y)])

        self._pen = QPen(QColor("green"), 2)

        try:
            base_image = Image.open(f'{self.map_scene.loading_manager.game_files}/UI/Maps/{map_zone["folder"]}/UI_CRB_Revealed/UI_CRB_Revealed.png')
            mask_image = Image.open(Path(__file__).resolve().parents[2] / "assets" / "region_alpha.png").convert("L")

            base_image.putalpha(mask_image)

            image_qt = ImageQt(base_image).copy()

            self._pixmap = QPixmap.fromImage(image_qt).scaled(
                QSize(round(max_x - min_x), round(max_x - min_x)),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            center = self._polygon.boundingRect().center()
            x = round(center.x() - (self._pixmap.width() / 2))
            y = round(center.y() - (self._pixmap.height() / 2))
            self._pixmap_rect = QRectF(x, y, self._pixmap.width(), self._pixmap.height())

        except FileNotFoundError as e:
            print(f"Error loading pixmap for region {map_zone['folder']}: {e}")

    def boundingRect(self):

        pad = self._pen.widthF() / 2.0
        bounds = self._polygon.boundingRect().adjusted(-pad, -pad, pad, pad)

        if self.map_zone['mapZoneIdParent']:
            bounds = bounds.united(self._pixmap_rect)

        return bounds

    def paint(self, painter, option, widget=None):

        if self.is_hovered:

            if self.map_zone['mapZoneIdParent']:
                if self._pixmap:
                    painter.drawPixmap(round(self._pixmap_rect.x()), round(self._pixmap_rect.y()), self._pixmap)
            #TODO
            else:
                painter.setPen(self._pen)
                painter.drawPolygon(self._polygon)

    def mousePressEvent(self, event):

        if self.is_hovered and self.content.get('Datacube'):
            self.map_scene.select_object(self)

        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):

        self.is_hovered = True

        self.update()

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):

        self.is_hovered = False

        self.update()

        super().hoverLeaveEvent(event)
