import ast
from pprint import pprint
from urllib.parse import unquote

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class ContentLabel(QLabel):

    def __init__(self, text: str, name: str, icon: str | None = None):
        super().__init__()

        self.icon = icon
        #Class name for stylesheet
        self.setObjectName(name)
        #Player input text
        if any(name.startswith(string) for string in ['LabelSay']):
            text = f'> <b>{text}</b>'

        self.setText(f'<div>{text}</div>')

        self.setMinimumWidth(425 - (10 * 2) + 1) #Window width + padding + threshold
        self.setWordWrap(True)
        #Handle links
        self.setOpenExternalLinks(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.linkActivated.connect(self.link_manager)
        self.linkHovered.connect(self.link_tooltip)
    """
    'creature' : model viewer

    'vitem' : tooltip
    'item' : tooltip
    'schematic' : tooltip

    'target' : 'TargetGroup' #TODO can be managed outside
    """
    def link_manager(self, link):

        decoded_link = ast.literal_eval(unquote(link))

        pprint(decoded_link)

        if any(decoded_link.get(enum) != None for enum in ['questPlayerFactionEnum', 'pathMissionTypeEnum']):

            from nexus_explorer.ui.content_viewer import ContentViewerWindow
            #Close old popup
            self.parent().close_popup()

            self.parent().popup = ContentViewerWindow(self.parent().loading_manager, decoded_link, self.parent().map_object)
            self.parent().popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.parent().popup.show()

        elif any(decoded_link.get(enum) != None for enum in ['CreationTypeEnum']):

            from nexus_explorer.ui.model_viewer import ModelViewerWindow
            #Close old popup
            self.parent().close_popup()

            self.parent().popup = ModelViewerWindow(self.parent().loading_manager, decoded_link)
            self.parent().popup.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.parent().popup.show()

    def link_tooltip(self, link):
        pass
        # decoded_link = ast.literal_eval(unquote(link))
        # print(decoded_link)
