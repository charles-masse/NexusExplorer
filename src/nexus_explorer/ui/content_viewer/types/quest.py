from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow
    
def display_quest(window: "ContentViewerWindow"):
    #TODO faction?
    content = window.content

    for string in [
        'localizedTextIdText',
        'localizedTextIdGiverTextUnknown',
        *[s for i in range(5) for s in [f'localizedTextIdMoreInfoSay0{i}', f'localizedTextIdMoreInfoText0{i}']],
        'localizedTextIdAcceptResponse',
        'localizedTextIdGiverSayAccepted'
    ]:
        window.add_label(content.get(string), 'LabelInfo')

    pos = window.loading_manager['WorldLocation2'].get(content['WorldLocation2IdReceiver'])
    if pos:
        window.add_map_location((pos['position0'], pos['position2']), str(-1))
    #Objectives
    for i in reversed(range(6)):

        objective_id = content.get(f"objective0{'' if i == 0 else i}") #fix for the strange naming in the db
        if objective_id:
            objective_data = window.loading_manager['QuestObjective'].get(objective_id)

            if objective_data:

                window.add_label(objective_data['localizedTextIdFull'], 'LabelObjective')

                for x in range(4):
                    pos = window.loading_manager['WorldLocation2'].get(objective_data[f'worldLocationsIdIndicator0{x}'])
                    if pos:
                        window.add_map_location((pos['position0'], pos['position2']), str(i + 1))

                directions = window.loading_manager['QuestDirection'].get(objective_data['questDirectionId'])
                if directions:
                    for x in range(16):
                        entry_id = directions.get(f'questDirectionEntryId{str(x).zfill(2)}')
                        dir = window.loading_manager['QuestDirectionEntry'].get(entry_id)
                        if dir:
                            loc = window.loading_manager['WorldLocation2'].get(dir['worldLocation2Id'])
                            if loc:
                                window.add_map_location((loc['position0'], loc['position2']), str(i + 1))

    for string in [
        'localizedTextIdReceiverTextAchieved',
        'localizedTextIdCompleteResponse',
        'localizedTextIdReceiverSayCompleted',
        'localizedTextIdCompletedSummary'
    ]:
        window.add_label(content.get(string), 'LabelInfo')
