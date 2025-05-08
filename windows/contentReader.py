
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from singletons import LocalizedStrings
from actions.links import linkGameObject

from pprint import pprint # DEBUG

class Window(QWidget):

    def __init__(self, data):
        super().__init__()

        pprint(data)

        self.setWindowTitle(LocalizedStrings[data.get('localizedTextIdTitle')])

        layout = QVBoxLayout()
        self.setLayout(layout)
        # Quest
        text = LocalizedStrings[data.get('localizedTextIdText')]

        if text and '$' in text:
            text = linkGameObject(text)

        label = QLabel(f'<div>{text}</div>')

        label.setWordWrap(True)
        # Click on link
        label.setOpenExternalLinks(False)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        def handleLink(link):
            test = eval(link)
            pprint(test)

        label.linkActivated.connect(handleLink)

        layout.addWidget(label)

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.setFixedSize(400, label.height() + 25)
        self.move(screen.x(), screen.y())

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
