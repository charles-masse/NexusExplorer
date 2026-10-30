from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow
    
def display_quest(window: "ContentViewerWindow"):
    #TODO completion loc, faction?
    content = window.content
    loading_manager = window.loading_manager

    for text in [
        ('localizedTextIdText', 'LabelInfo'),
        ('localizedTextIdGiverTextUnknown', 'LabelRespond'),
        *[s for i in range(5) for s in [(f'localizedTextIdMoreInfoSay0{i}', 'LabelSay'), (f'localizedTextIdMoreInfoText0{i}', 'LabelRespond')]],
        ('localizedTextIdAcceptResponse', 'LabelSay'),
        ('localizedTextIdGiverSayAccepted', 'LabelRespond')
    ]:
        window.add_label(content.get(text[0]), text[1])
    #Objectives
    for i in reversed(range(6)):

        objective_id = content.get(f"objective0{'' if i == 0 else i}")
        if objective_id:
            objective_data = loading_manager['QuestObjective'].get(objective_id)

            if objective_data:

                window.add_label(objective_data['localizedTextIdFull'], 'LabelObjective')

                for x in range(4):
                    pos = loading_manager['WorldLocation2'].get(objective_data[f'worldLocationsIdIndicator0{x}'])
                    if pos:
                        window.add_map_location(pos, str(i + 1))

                directions = loading_manager['QuestDirection'].get(objective_data['questDirectionId'])
                if directions:
                    for x in range(16):
                        entry_id = directions.get(f'questDirectionEntryId{str(x).zfill(2)}')
                        dir = loading_manager['QuestDirectionEntry'].get(entry_id)
                        if dir:
                            loc = loading_manager['WorldLocation2'].get(dir['worldLocation2Id'])
                            if loc:
                                window.add_map_location(loc, str(i + 1))

    for text in [
        ('localizedTextIdReceiverTextAchieved', 'LabelRespond'),
        ('localizedTextIdCompleteResponse', 'LabelSay'),
        ('localizedTextIdReceiverSayCompleted', 'LabelRespond'),
        ('localizedTextIdCompletedSummary', 'LabelInfo')
    ]:
        window.add_label(content.get(text[0]), text[1])
    #Start location #TODO alt receivers
    pos = loading_manager['WorldLocation2'].get(content['WorldLocation2IdReceiver'])
    if pos:
        window.add_map_location(pos, str(-2))
