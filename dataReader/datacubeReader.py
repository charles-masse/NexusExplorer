
from pprint import pprint

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class window(QWidget):

    def __init__(self, data):
        super().__init__()

        pprint(data)

        self.setWindowTitle(data['localizedTextIdTitle'])

        layout = QVBoxLayout()
        self.setLayout(layout)

        text = ''.join([data['localizedTextIdText0%i' % textId] for textId in range(6) if data['localizedTextIdText0' + str(textId)]])

        layout.addWidget(QPlainTextEdit(text.replace(r'\n', '\n')))

        screen = QApplication.primaryScreen().geometry()
        self.setFixedSize(400, 250)

        self.show()
