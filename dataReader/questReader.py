
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

        # Summary of the quest
        layout.addWidget(QPlainTextEdit(data['localizedTextIdText']))

        # In-character explanation
        startText = data['localizedTextIdGiverTextUnknown']

        if startText:
            layout.addWidget(QPlainTextEdit(startText))

        # Extra infos
        for moreInfo in range(5):

            moreInfoSay = data['localizedTextIdMoreInfoSay0%i' % moreInfo]
            moreInfoText = data['localizedTextIdMoreInfoText0%i' % moreInfo]

            if moreInfoText:
                layout.addWidget(QLineEdit(moreInfoSay))
                layout.addWidget(QPlainTextEdit(moreInfoText))

        # Objectives
        for objective in range(6):

            try:
                objectiveText = data['objective%i' % objective]['localizedTextIdFull']
                layout.addWidget(QPlainTextEdit(objectiveText))

            except:
                pass

        # Summary of how the quest ends
        summaryEnd = data['localizedTextIdCompletedSummary']

        if summaryEnd:
            layout.addWidget(QPlainTextEdit(summaryEnd))

        print()

        self.setFixedSize(400, layout.count() * 100)

        self.show()
