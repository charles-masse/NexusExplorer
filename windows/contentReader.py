
from pprint import pprint

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

# class Challenge(QWidget):

#     def __init__(self, data):
#         super().__init__()

#         pprint(data)

#         self.setWindowTitle(data['localizedTextIdName'])

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         layout.addWidget(QPlainTextEdit(data['localizedTextIdProgress']))

#         screen = QApplication.primaryScreen().geometry()
#         self.setFixedSize(400, layout.count() * 100)

#         self.show()

# class datacube(QWidget):

#     def __init__(self, data):
#         super().__init__()

#         pprint(data)

#         self.setWindowTitle(data['localizedTextIdTitle'])

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         text = ''.join([data['localizedTextIdText0%i' % textId] for textId in range(6) if data['localizedTextIdText0' + str(textId)]])

#         layout.addWidget(QPlainTextEdit(text.replace(r'\n', '\n')))

#         screen = QApplication.primaryScreen().geometry()
#         self.setFixedSize(400, 250)

#         self.show()

# class event(QWidget):

#     def __init__(self, data):
#         super().__init__()

#         pprint(data)

#         self.setWindowTitle(data['localizedTextIdName'])

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         for objective in data['PublicEventObjective'].values():

#             try:
#                 objectiveText = objective['localizedTextId']
#                 layout.addWidget(QPlainTextEdit(objectiveText))

#             except:
#                 pass

#         end = data['localizedTextIdEnd']

#         if end:
#             layout.addWidget(QPlainTextEdit(end))

#         screen = QApplication.primaryScreen().geometry()
#         self.setFixedSize(400, layout.count() * 100)

#         self.show()

class Window(QWidget):

    def __init__(self, data):
        super().__init__()

        pprint(data)

        # self.setWindowTitle()

        # if contentType == 'QuestObjective':
        #     content = location.get('Quest2', {})
            
        # elif contentType == 'PublicEventObjective':
        #     content = location.get('publicEventId', {})

        # else:
        #     content = location

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(400, screen.height())
        self.move(screen.x(), screen.y())

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
