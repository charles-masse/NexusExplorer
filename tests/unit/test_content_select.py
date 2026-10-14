
import pytest

from nexus_explorer.data import LoadingManager  # type: ignore[import-untyped]
from nexus_explorer.ui import ContentSelectWindow  # type: ignore[import-untyped]
from nexus_explorer.ui.map_viewer.cluster import (  # type: ignore[import-untyped]
    LocationData,
)
from nexus_explorer.ui.map_viewer.objects import (  # type: ignore[import-untyped]
    LocationObject,
)
from nexus_explorer.ui.map_viewer.window import MapScene  # type: ignore[import-untyped]
from nexus_explorer.ui.world_select.utilities import (  # type: ignore[import-untyped]
    WorldData,
)


@pytest.fixture
def loading_manager():
    return LoadingManager('tests/sample_data')
#UI
@pytest.fixture
def world_select_window(loading_manager, qtbot):

    scene = MapScene(loading_manager, WorldData('0', '', 'TestWorld'))
    widget = ContentSelectWindow(loading_manager, LocationObject(LocationData(0, 0), scene))
    qtbot.addWidget(widget)

    return widget

def test_world_select(world_select_window):
    world_select_window.show()
