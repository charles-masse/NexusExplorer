
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def display_challenge(window: "ContentViewerWindow"):
    """ challengeTypeEnum
    0 - Kill
    1 - Use item
    2 - Race (often has a start and end)
    3 - —
    4 - Collect
    5 - Collect
    6 - —
    7 - Race to interact
    """
    content = window.content
    #Challenge description
    window.add_label(content.get('localizedTextIdProgress'), 'LabelInfo')
    #Link item
    # if content['challengeTypeEnum'] == 1:
    #     pass #TODO add item
    #Tiers
    for tier in range(3):

        tier_id = content.get(f'challengeTierId0{tier}', 0)
        tier_data = window.loading_manager['ChallengeTier'].get(tier_id)
        if tier_data:
            tier_threshold = tier_data['count']
            #Races - Milliseconds to seconds #TODO not always a race
            # if content['challengeTypeEnum'] in [2, 7]:
            #     tier_threshold = f'{int(tier_threshold / 1000)} seconds'

            window.add_label(str(tier_threshold), f'LabelChallenge{tier}')
    #Map icons
    indicator = window.loading_manager['WorldLocation2'].get(content['worldLocation2IdIndicator'])
    if indicator:
        window.add_map_location((indicator['position0'], indicator['position2']), '★')

    start = window.loading_manager['WorldLocation2'].get(content['worldLocation2IdStartLocation'])
    if start:
        window.add_map_location((start['position0'], start['position2']), '-1')

    direction_data = window.loading_manager['QuestDirection']
    directions = direction_data.get(content['questDirectionIdActive'])
    if directions:
        for x in range(16):

            entry_id = directions.get(f'questDirectionEntryId{str(x).zfill(2)}')
            dir = window.loading_manager['QuestDirectionEntry'].get(entry_id)
            if dir:
                loc = window.loading_manager['WorldLocation2'].get(dir['worldLocation2Id'])
                if loc:
                    window.add_map_location((loc['position0'], loc['position2']), str(x + 1))
