from typing import TYPE_CHECKING

from nexus_explorer.ui.content_viewer.labels import ContentLabel

from .explorer import (
    explorer_cartography,
    explorer_exploration,
    explorer_operation,
    explorer_scavenger,
    explorer_stalking,
    explorer_vista,
)
from .scientist import (
    scientist_analysis,
    scientist_datacube,
    scientist_experimentation,
    scientist_speciment,
    scientist_study,
)
from .settler import (
    settler_cache,
    settler_expansion,
    settler_project,
    settler_safety,
    settler_service,
)
from .soldier import (
    soldier_assassinate,
    soldier_demolition,
    soldier_rescue,
    soldier_security,
    soldier_SWAT,
)

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow


def display_mission(window: "ContentViewerWindow"):
    content = window.content

    unlock = content.get('localizedTextIdUnlock')
    if unlock:
        window.right_layout.addWidget(ContentLabel(unlock, 'localizedTextIdUnlock'))
    #Soldier orders
    if content.get('pathTypeEnum') == 0:
        soldier_orders = content.get('localizedTextIdSoldierOrders')
        if soldier_orders:
            window.right_layout.addWidget(ContentLabel(soldier_orders, 'localizedTextIdSoldierOrders'))
    #Mission type specific
    mission_id = content['pathMissionTypeEnum']

    if mission_id in [0]:
        soldier_security(window)
    elif mission_id in [2, 14]:
        scientist_analysis(window)
    elif mission_id in [3]:
        explorer_stalking(window)
    elif mission_id in [4]:
        soldier_assassinate(window)
    elif mission_id in [5]:
        soldier_demolition(window)
    elif mission_id in [6]:
        soldier_rescue(window)
    elif mission_id in [7]:
        soldier_SWAT(window)
    elif mission_id in [12]:
        explorer_exploration(window)
    elif mission_id in [13, 18]:
        explorer_scavenger(window)
    elif mission_id in [15]:
        explorer_vista(window)
    elif mission_id in [16]:
        explorer_cartography(window)
    elif mission_id in [17]:
        explorer_operation(window)
    elif mission_id in [19]:
        settler_expansion(window)
    elif mission_id in [20]:
        scientist_study(window)
    elif mission_id in [21]:
        settler_project(window)
    elif mission_id in [22]:
        scientist_experimentation(window)
    elif mission_id in [23]:
        scientist_speciment(window)
    elif mission_id in [24]:
        scientist_datacube(window)
    elif mission_id in [25]:
        settler_service(window)
    elif mission_id in [26]:
        settler_safety(window)
    elif mission_id in [27]:
        settler_cache(window)
    else:
        raise TypeError(f'Cannot parse this path mission id {mission_id}.')

    comms = content.get('localizedTextIdCommunicator')
    if comms:
        window.right_layout.addWidget(ContentLabel(comms, 'localizedTextIdCommunicator'))
