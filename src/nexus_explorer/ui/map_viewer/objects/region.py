
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
    def __init__(self, map_zone: dict, contents: dict, map_scene: "MapScene"):
        super().__init__()

        self.map_zone = map_zone
        self.contents = contents
        self.map_scene = map_scene

        self.name = self.contents.get('localizedTextIdName', 'Untitled Region')

        self.setAcceptHoverEvents(True)
        self.is_hovered = False
        
        self._pixmap = None
        self._pixmap_rect = QRectF()
        # Create polygon
        min_x, min_y = world_to_screen_pos(
            *hex_to_world_coordinates(self.map_zone["hexMinX"] - 1, self.map_zone["hexMinY"] - 0.5)
        )
        max_x, max_y = world_to_screen_pos(
            *hex_to_world_coordinates(self.map_zone["hexLimX"] + 1, self.map_zone["hexLimY"] + 1)
        )
        self._polygon = QPolygonF(
            [
                QPointF(min_x, min_y),
                QPointF(max_x, min_y),
                QPointF(max_x, max_y),
                QPointF(min_x, max_y),
            ]
        )

        self._pen = QPen(QColor("green"), 2)

        try:
            base_image = Image.open(
                f'{self.map_scene.loading_manager.game_files}/UI/Maps/{map_zone["folder"]}/UI_CRB_Revealed/UI_CRB_Revealed.png'
            )
            mask_image = Image.open(
                Path(__file__).resolve().parents[3] / "assets" / "region_alpha.png"
            ).convert("L")

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
            print(f"Error loading region map for {self.map_zone['folder']}. -SKIPPED-")

    def boundingRect(self):
        pad = self._pen.widthF() / 2.0
        bounds = self._polygon.boundingRect().adjusted(-pad, -pad, pad, pad)

        if self.map_zone["mapZoneIdParent"]:
            bounds = bounds.united(self._pixmap_rect)

        return bounds

    def paint(self, painter, option, widget = None):

        if self.map_zone["mapZoneIdParent"]:
            if self._pixmap:
                painter.drawPixmap(
                    round(self._pixmap_rect.x()),
                    round(self._pixmap_rect.y()),
                    self._pixmap,
                )
        # else: #TODO
        #     painter.setPen(self._pen)
        #     painter.drawPolygon(self._polygon)

        if self.is_hovered and painter:
            self.setOpacity(1)
        else:
            self.setOpacity(0.5)

    def mousePressEvent(self, event):
        if self.is_hovered:
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
