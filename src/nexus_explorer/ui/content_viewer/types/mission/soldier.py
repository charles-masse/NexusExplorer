
from typing import TYPE_CHECKING

from nexus_explorer.ui.content_viewer.labels import ContentLabel

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow


def soldier_security(window: "ContentViewerWindow"):  #'PathSoldierEventWave' ??? Wave info probably server side
    pass

def soldier_assassinate(window: "ContentViewerWindow"):

    content = window.content

    assassination = window.loading_manager['PathSoldierAssassinate'].get(content['objectId'])
    if assassination:
        window.right_layout.addWidget(ContentLabel(f"Assassinate {assassination['count']} $(creature={assassination['creature2Id']})", 'PathObjective'))

def soldier_demolition(window: "ContentViewerWindow"):

    content = window.content

    demolition = window.loading_manager['PathSoldierActivate'].get(content['objectId'])
    if demolition:
        window.right_layout.addWidget(ContentLabel(f"Assassinate {demolition['count']} $(creature={demolition['creature2Id']})", 'PathObjective'))

def soldier_rescue(window: "ContentViewerWindow"):

    content = window.content

    rescue = window.loading_manager['PathSoldierActivate'].get(content['objectId'])
    if rescue:
        window.right_layout.addWidget(ContentLabel(f"Rescue {rescue['count']} $(creature={rescue['creature2Id']})", 'PathObjective'))

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

            if creatureId != '0':
                creatures.append(f"$(creature={creatureId})")

        group_name = ', '.join(list(set(creatures)))

    else:
        group_name = f'<i>{group_name}</i>'

    window.right_layout.addWidget(ContentLabel(f"Kill {swat['count']} {group_name} with $(vitem={swat['virtualItemIdDisplay']})", 'PathObjective'))
