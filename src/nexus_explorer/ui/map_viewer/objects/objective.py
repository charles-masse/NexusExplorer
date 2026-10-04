
from PyQt6.QtGui import QColor, QFont, QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsTextItem


class ObjectiveObject(QGraphicsPixmapItem):
    def __init__(self, objectiveId: int, game_files: str):
        super().__init__()
        # TODO
        # position = world_to_screen_pos(x, y) #TODO include in icon class
        # obj.setPos(position[0] - (obj.im.width() / 2), position[1] - (obj.im.height() / 2))

        self.im = QPixmap(
            f"{game_files}/UI/Assets/TexPieces/UI_CRB_HUD_Tracker_349_73/UI_CRB_HUD_Tracker_349_73.png"
        )
        self.setPixmap(self.im)

        text = QGraphicsTextItem(str(objectiveId), self)
        text.setDefaultTextColor(QColor("white"))
        text.setFont(QFont(f"{game_files}/UI/Fonts/segoeuib.ttf", 10))

        text_rect = text.boundingRect()
        text.setPos((self.im.width() / 2) - (text_rect.width() / 2), 0)
