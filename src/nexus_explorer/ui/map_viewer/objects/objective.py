from pathlib import Path

from PyQt6.QtGui import QColor, QFont, QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsTextItem

from ..utilities import world_to_screen_pos


class ObjectiveObject(QGraphicsPixmapItem):
    def __init__(self, objectiveId: str, pos):
        super().__init__()

        self.setZValue(2)

        if objectiveId == '-1':
            im = QPixmap(str(Path(__file__).resolve().parents[3] / "assets" / "icon_start.png"))
            self.setPixmap(im)

        elif objectiveId == '-2':
            im = QPixmap(str(Path(__file__).resolve().parents[3] / "assets" / "icon_quest.png"))
            self.setPixmap(im)

        else:
            im = QPixmap(str(Path(__file__).resolve().parents[3] / "assets" / "icon_objective.png"))
            self.setPixmap(im)

            text = QGraphicsTextItem(objectiveId, self)
            text.setDefaultTextColor(QColor("white"))
            text.setFont(QFont(str(Path(__file__).resolve().parents[3] / "assets" / "segoeuib.ttf"), 8))

            text_rect = text.boundingRect()
            text.setPos(
                (im.width() - text_rect.width()) / 2,
                (im.height() - text_rect.height()) / 2,
            )

        position = world_to_screen_pos(*pos)
        self.setPos(position[0] - (im.width() / 2), position[1] - (im.height() / 2))
