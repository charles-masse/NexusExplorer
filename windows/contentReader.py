
from pprint import pprint

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class Window(QWidget):

    def __init__(self, data):
        super().__init__()

        pprint(data)

        # self.setWindowTitle(data['localizedTextIdTitle'])

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(400, screen.height())
        self.move(screen.x(), screen.y())

        layout = QVBoxLayout()
        self.setLayout(layout)
        # Quest

        # layout.addWidget(QPlainTextEdit(data['localizedTextIdText']))
        # # In-character explanation
        # startText = data['localizedTextIdGiverTextUnknown']

        # if startText:
        #     layout.addWidget(QPlainTextEdit(startText))
        # # Extra infos
        # for moreInfo in range(5):

        #     moreInfoSay = data['localizedTextIdMoreInfoSay0%i' % moreInfo]
        #     moreInfoText = data['localizedTextIdMoreInfoText0%i' % moreInfo]

        #     if moreInfoText:
        #         layout.addWidget(QLineEdit(moreInfoSay))
        #         layout.addWidget(QPlainTextEdit(moreInfoText))
        # # Objectives
        # for objective in range(6):
        #     try:
        #         objectiveText = data['objective%i' % objective]['localizedTextIdFull']
        #         layout.addWidget(QPlainTextEdit(objectiveText))

        #     except:
        #         pass
        # # Summary of how the quest ends
        # summaryEnd = data['localizedTextIdCompletedSummary']

        # Get parent
        # if contentType == 'QuestObjective':
        #     content = location.get('Quest2', {})
            
        # elif contentType == 'PublicEventObjective':
        #     content = location.get('publicEventId', {})

        # else:
        #     content = location

        # Challenge
        # layout.addWidget(QPlainTextEdit(data['localizedTextIdProgress']))

        # Datacube
        # text = ''.join([data['localizedTextIdText0%i' % textId] for textId in range(6) if data['localizedTextIdText0' + str(textId)]])
        # layout.addWidget(QPlainTextEdit(text.replace(r'\n', '\n')))

        # Event
        # for objective in data['PublicEventObjective'].values():

        #     try:
        #         objectiveText = objective['localizedTextId']
        #         layout.addWidget(QPlainTextEdit(objectiveText))

        #     except:
        #         pass

        #     end = data['localizedTextIdEnd']

        # if summaryEnd:
        #     layout.addWidget(QPlainTextEdit(summaryEnd))
