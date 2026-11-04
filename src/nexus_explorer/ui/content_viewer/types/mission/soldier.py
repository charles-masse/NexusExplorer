
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def soldier_security(window: "ContentViewerWindow"):
    #TODO
    content = window.content
    loading_manager = window.loading_manager

    # for creature in loading_manager['Creature2'].values():
    #     if creature['pathMissionIdSoldier'] == content['ID']:
    #         break

def soldier_assassinate(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager

    assassination = loading_manager['PathSoldierAssassinate'].get(content['objectId'])
    if assassination:
        #Creature or target group
        if assassination['creature2Id']:
            target = f'$(creature={assassination['creature2Id']})'
        else:
            target = f'$(target={assassination['targetGroupId']})'
        #Count
        if assassination['count'] > 1 or assassination['targetGroupId']:
            count = str(assassination['count']) + ' '
        else:
            count = ''

        window.add_label(f"Assassinate {count}{target}", 'LabelObjective')
    #Target location
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '1')

def soldier_demolition(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager

    demolition = loading_manager['PathSoldierActivate'].get(content['objectId'])
    if demolition:
        #Creature or target group
        if demolition['creature2Id']:
            target = f'$(creature={demolition['creature2Id']})'
        else:
            target = f'$(target={demolition['targetGroupId']})'
        #Count
        if demolition['count'] > 1 or demolition['targetGroupId']:
            count = str(demolition['count']) + ' '
        else:
            count = ''

        window.add_label(f"Demolish {count}{target}", 'LabelObjective')
    #Target location
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '1')

def soldier_rescue(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager

    rescue = loading_manager['PathSoldierActivate'].get(content['objectId'])
    if rescue:
        #Creature or target group
        if rescue['creature2Id']:
            target = f'$(creature={rescue['creature2Id']})'
        else:
            target = f'$(target={rescue['targetGroupId']})'
        #Count
        if rescue['count'] > 1 or rescue['targetGroupId']:
            count = str(rescue['count']) + ' '
        else:
            count = ''

        window.add_label(f"Rescue {count}{target}", 'LabelObjective')
    #Target location
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '1')

def soldier_SWAT(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager

    swat = loading_manager['PathSoldierSWAT'].get(content['objectId'])
    if swat:
        #Creature or target group
        if swat['creature2Id']:
            target = f'$(creature={swat['creature2Id']})'
        else:
            target = f'$(target={swat['targetGroupId']})'
        #Count
        if swat['count'] > 1 or swat['targetGroupId']:
            count = str(swat['count']) + ' '
        else:
            count = ''

        window.add_label(f"Use $(vitem={swat['virtualItemIdDisplay']}) on {count}{target}", 'LabelObjective')
    #Target location
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '1')
