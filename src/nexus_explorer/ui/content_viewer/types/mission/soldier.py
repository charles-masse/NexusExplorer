
from typing import TYPE_CHECKING

from ..utilities import add_mission_locations, get_mission_context, get_target_group

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def soldier_security(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)
    # loading_manager = window.loading_manager

    # for creature in loading_manager['Creature2'].values():
    #     if creature['pathMissionIdSoldier'] == content['ID']:
    #         break

    window.add_label("Defend.", 'LabelObjective')
    #Target location
    add_mission_locations(window, content, '1')

def soldier_assassinate(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    assassination = loading_manager['PathSoldierAssassinate'].get(content['objectId'])
    if assassination:
        #Creature or target group
        if assassination['creature2Id']:
            target = f'$(creature={assassination['creature2Id']})'

        else:
            target = get_target_group(loading_manager, assassination['targetGroupId'])
        #Count
        if assassination['count'] > 1 or assassination['targetGroupId']:
            count = str(assassination['count']) + ' '

        else:
            count = ''

        window.add_label(f"Assassinate {count}{target}", 'LabelObjective', assassination['count'])
    #Target location
    add_mission_locations(window, content, '1')

def soldier_demolition(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    demolition = loading_manager['PathSoldierActivate'].get(content['objectId'])
    if demolition:
        #Creature or target group
        if demolition['creature2Id']:
            target = f'$(creature={demolition['creature2Id']})'

        else:
            target = get_target_group(loading_manager, demolition['targetGroupId'])
        #Count
        if demolition['count'] > 1 or demolition['targetGroupId']:
            count = str(demolition['count']) + ' '

        else:
            count = ''

        window.add_label(f"Demolish {count}{target}", 'LabelObjective', demolition['count'])
    #Target location
    add_mission_locations(window, content, '1')

def soldier_rescue(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    rescue = loading_manager['PathSoldierActivate'].get(content['objectId'])
    if rescue:
        #Creature or target group
        if rescue['creature2Id']:
            target = f'$(creature={rescue['creature2Id']})'

        else:
            target = get_target_group(loading_manager, rescue['targetGroupId'])
        #Count
        if rescue['count'] > 1 or rescue['targetGroupId']:
            count = str(rescue['count']) + ' '

        else:
            count = ''

        window.add_label(f"Rescue {count}{target}", 'LabelObjective', rescue['count'])
    #Target location
    add_mission_locations(window, content, '1')

def soldier_SWAT(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

    swat = loading_manager['PathSoldierSWAT'].get(content['objectId'])
    if swat:
        #Creature or target group
        if swat['creature2Id']:
            target = f'$(creature={swat['creature2Id']})'

        else:
            target = get_target_group(loading_manager, swat['targetGroupId'])
        #Count
        if swat['count'] > 1 or swat['targetGroupId']:
            count = str(swat['count']) + ' '

        else:
            count = ''

        window.add_label(f"Use $(vitem={swat['virtualItemIdDisplay']}) on {count}{target}", 'LabelObjective', swat['count'])
    #Target location
    add_mission_locations(window, content, '1')
