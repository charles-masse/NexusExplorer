
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import QPointF, QRectF, QSize, Qt
from PyQt6.QtGui import QColor, QPen, QPixmap, QPolygonF
from PyQt6.QtWidgets import QGraphicsObject

from ..utilities import hex_to_world_coordinates, world_to_screen_pos

if TYPE_CHECKING:
    from ..window import MapScene

class RegionObject(QGraphicsObject):
    def __init__(self, contents: dict, map_scene: "MapScene"):
        super().__init__()

        self.contents = contents
        self.map_scene = map_scene
        
        self.is_hovered = False
        self.display_override = False

        self.setAcceptHoverEvents(True)

        map_scene.display_locations(self.contents.get('WorldLocation2', []), self)

        if all(zone["mapZoneIdParent"] for zone in self.contents["MapZone"]) and not self.contents.get('WorldLocation2'):
            self.hide()

        self.name = self.contents.get('localizedTextIdName', 'Untitled Region')

        self._pixmap = None
        self._pixmap_rect = QRectF()
        #Find biggest zone
        map_zones = self.contents['MapZone']
        largest_zone = max(
            map_zones,
            key=lambda x: (
                (x["hexLimX"] - x["hexMinX"]) *
                (x["hexLimY"] - x["hexMinY"])
            )
        )       
        #Create polygon
        min_x, min_y = world_to_screen_pos(
            *hex_to_world_coordinates(largest_zone["hexMinX"] - 1, largest_zone["hexMinY"])
        )
        max_x, max_y = world_to_screen_pos(
            *hex_to_world_coordinates(largest_zone["hexLimX"] + 1, largest_zone["hexLimY"] + 0.5)
        )

        self._polygon = QPolygonF(
            [
                QPointF(min_x, max_y),
                QPointF(max_x, max_y),
                QPointF(max_x, min_y),
                QPointF(min_x, min_y),
            ]
        )

        self._pen = QPen(QColor("green"), 2)

        try:
            base_image = Image.open(f'{self.map_scene.loading_manager.game_files}/UI/Maps/{largest_zone["folder"]}/UI_CRB_Revealed/UI_CRB_Revealed.png')
            mask_image = Image.open(Path(__file__).resolve().parents[3] / "assets" / "region_alpha.png").convert("L")
            base_image.putalpha(mask_image)

            image_qt = ImageQt(base_image).copy()

            self._pixmap = QPixmap.fromImage(image_qt).scaled(
                QSize(round(max_x - min_x), round(max_x - min_x)),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            center = self._polygon.boundingRect().center()
            x = round(center.x() - (self._pixmap.width() / 2))
            y = round(center.y() - (self._pixmap.height() / 2))
            self._pixmap_rect = QRectF(x, y, self._pixmap.width(), self._pixmap.height())

        except FileNotFoundError:
            print(f"Error loading region map for {largest_zone['folder']}. -SKIPPED-")

    def boundingRect(self):
        pad = self._pen.widthF() / 2.0
        bounds = self._polygon.boundingRect().adjusted(-pad, -pad, pad, pad)

        if all(zone["mapZoneIdParent"] for zone in self.contents["MapZone"]):
            bounds = bounds.united(self._pixmap_rect)

        return bounds

    def paint(self, painter, option, widget=None):

        if all(zone["mapZoneIdParent"] for zone in self.contents["MapZone"]):
            if self._pixmap:
                painter.drawPixmap(
                    round(self._pixmap_rect.x()),
                    round(self._pixmap_rect.y()),
                    self._pixmap,
                )
        else: #TODO Hex border
            painter.setPen(self._pen)
            painter.drawPolygon(self._polygon)

        if self.is_hovered or self.display_override:
            opacity = 1
        else:
            opacity = 0.6

        self.setOpacity(opacity)
        for child in self.children():
            child.setOpacity(opacity)

    def mousePressEvent(self, event):

        if self.is_hovered and not all(zone["mapZoneIdParent"] for zone in self.contents["MapZone"]):
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
