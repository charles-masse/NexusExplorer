
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from nexus_explorer.ui.content_viewer.labels import ContentLabel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow


def display_datacube(window: "ContentViewerWindow"):

    content = window.content

    datacube_text = []
    """
    0 - Voice-acted
    1 - with image (TfBtF)
    2 - Text-only
    """
    datacube_type_id = content['datacubeTypeEnum']
    
    if datacube_type_id == 0:
        pass #TODO Play sound
    
    if datacube_type_id == 1:

        image = content.get('assetPathImage')
        if image:
            image_file = image.replace('Icon_ItemTBF_', '')

            label = QLabel()
            pixmap = QPixmap(f'{window.loading_manager.game_files}/UI/Icon/Item/TBF/{image_file}/{image_file}.png')
            label.setPixmap(pixmap)
            window.main_layout.addWidget(label)
        else:
            print("Couldn't find image.")
    
    for datacube_string_id in range(6):

        datacub_string = content.get(f'localizedTextIdText0{datacube_string_id}')

        if datacub_string:
            datacube_text.append(datacub_string)

    window.main_layout.addWidget(ContentLabel('\n'.join(datacube_text), 'QuestObjective'))
