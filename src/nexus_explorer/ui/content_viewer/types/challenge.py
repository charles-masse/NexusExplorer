
from pprint import pprint
from typing import TYPE_CHECKING

from nexus_explorer.ui.content_viewer.labels import ContentLabel

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_challenge(window: "ContentViewerWindow"):
    #TODO target? quest direction, items
    content = window.content
    #TYPE 0 = Kill 1= ??? 2 = race 4 = pickup? 5 = ??? 7 = ???
    pprint(content)

    text = content.get('localizedTextIdProgress')
    if text:
        window.right_layout.addWidget(ContentLabel(text, 'localizedTextIdEnd'))
    #Tiers
    for tier in range(3):

        tier_id = content.get(f'challengeTierId0{tier}')
        tier = window.loading_manager['ChallengeTier'].get(tier_id)

        if tier:
            window.right_layout.addWidget(ContentLabel(str(tier['count']), 'localizedTextIdEnd'))
