
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow


def soldier_security(window: "ContentViewerWindow"):  #'PathSoldierEventWave' ??? Wave info probably server side
    pass

def soldier_assassinate(window: "ContentViewerWindow"):

    content = window.content

    assassination = window.loading_manager['PathSoldierAssassinate'].get(content['objectId'])
    window.add_label(f"Assassinate {assassination['count']} $(creature={assassination['creature2Id']})", 'LabelObjective')

def soldier_demolition(window: "ContentViewerWindow"):

    content = window.content

    demolition = window.loading_manager['PathSoldierActivate'].get(content['objectId'])
    window.add_label(f"Destroy {demolition['count']} $(creature={demolition['creature2Id']})", 'LabelObjective')

def soldier_rescue(window: "ContentViewerWindow"):

    content = window.content

    rescue = window.loading_manager['PathSoldierActivate'].get(content['objectId'])
    window.add_label(f"Rescue {rescue['count']} $(creature={rescue['creature2Id']})", 'LabelObjective')

def soldier_SWAT(window: "ContentViewerWindow"):

    content = window.content

    swat = window.loading_manager['PathSoldierSWAT'].get(content['objectId'])
    group = window.loading_manager['TargetGroup'].get(swat['targetGroupId'])

    group_name = None
    
    if group:
        group_name = group['localizedTextIdDisplayString']
    
    if not group_name:

        creatures = []

        for i in range(7):
            
            creatureId = group[f'data{i}']
            if creatureId:
                creatures.append(f"$(creature={creatureId})")

        group_name = ', '.join(list(set(creatures)))

    else:
        group_name = f'<i>{group_name}</i>'

    window.add_label(f"Kill {swat['count']} {group_name} with $(vitem={swat['virtualItemIdDisplay']})", 'LabelObjective')
