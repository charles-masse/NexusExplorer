
from pprint import pprint

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class window(QWidget):

    def __init__(self, data):
        super().__init__()

        pprint(data)

        self.setWindowTitle(data['localizedTextIdName'])

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QPlainTextEdit(data['localizedTextIdProgress']))

        screen = QApplication.primaryScreen().geometry()
        self.setFixedSize(400, layout.count() * 100)

        self.show()
