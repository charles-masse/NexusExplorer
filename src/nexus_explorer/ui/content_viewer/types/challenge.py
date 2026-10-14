
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_challenge(window: "ContentViewerWindow"):
    #TODO type?, target, flag?, quest directions, items
    #The location string seems to be the same as the actual location name in most cases--double-check
    window.add_label('localizedTextIdProgress')
