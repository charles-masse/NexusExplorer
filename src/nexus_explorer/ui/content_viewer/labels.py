
import ast
import re
from urllib.parse import unquote

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class ContentLabel(QLabel):

    def __init__(self, text: str, name: str, number: int = 1, icon: str | None = None):
        super().__init__()

        self.icon = icon

        self.setObjectName(name)
        #PC dialog
        if any(name.startswith(string) for string in ['LabelSay']):
            text = f'> <b>{text}</b>'
        #Singular vs Plural
        for match in [m for m in re.finditer(r'([A-Za-z0-9 ]+)(?:\{\w+:([A-Za-z0-9 ]+)\})?', text) if m.group(2)]:

            full_match = match.group(0)

            print(match.group(0))

            if number == 1:
                singular = match.group(1)
                text = text.replace(full_match, singular)

            else:
                plural = match.group(2) or match.group(1)
                text = text.replace(full_match, plural)

        self.setText(f'<div>{text}</div>')

        self.setMinimumWidth(425 - (10 * 2) + 1) #Window width + padding + threshold
        self.setWordWrap(True)
        #Handle links
        self.setOpenExternalLinks(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.linkActivated.connect(self.link_manager)
        # self.linkHovered.connect(self.link_tooltip)
    """
    'creature' : model viewer
    'vitem' : tooltip
    'item' : tooltip
    'schematic' : tooltip
    'location' : select on map
    """
    def link_manager(self, link):
        #TODO Link location on map
        decoded_link = ast.literal_eval(unquote(link))

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

    # def link_tooltip(self, link):
    #     pass
    #     # decoded_link = ast.literal_eval(unquote(link))
    #     # print(decoded_link)
