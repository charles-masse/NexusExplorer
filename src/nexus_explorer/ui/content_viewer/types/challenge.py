
from typing import TYPE_CHECKING

from nexus_explorer.ui.content_viewer.labels import ContentLabel

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_challenge(window: "ContentViewerWindow"):
    """ challengeTypeEnum
    0 - Kill
    1 - Use item
    2 - Race
    3 - —
    4 - Collect
    5 - Collect
    6 - —
    7 - Race to interact
    """ #TODO quest directions, worldLocation2IdIndicator, worldLocation2IdStartLocation
    content = window.content

    text = content.get('localizedTextIdProgress')
    if text:
        window.right_layout.addWidget(ContentLabel(text, 'localizedTextIdEnd'))
    #Link item
    if content['challengeTypeEnum'] == 1:
        pass #TODO add item
    #Tiers
    for tier in range(3):

        tier_id = content.get(f'challengeTierId0{tier}', 0)
        tier_data = window.loading_manager['ChallengeTier'].get(tier_id)

        if tier_data:
            tier_threshold = tier_data['count']
            #Races - Milliseconds to seconds #TODO not always a race
            # if content['challengeTypeEnum'] in [2, 7]:
            #     tier_threshold = f'{int(tier_threshold / 1000)} seconds'

            window.right_layout.addWidget(ContentLabel(str(tier_threshold), f'challengeTierId0{tier}'))

    #TODO might be interesting, but it's for the whole region
    # reward_id = content.get('rewardTrackId', 0)
    # window.loading_manager['RewardTrack'].get(reward_id)
