import pytest

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
def content_select_window(loading_manager, qtbot):
    scene = MapScene(loading_manager, WorldData("0", "", "TestWorld"))
    location = LocationObject(
        LocationData(**loading_manager["WorldLocation2"].get(1)),
        scene,
    )
    widget = ContentSelectWindow(loading_manager, location)
    qtbot.addWidget(widget)
    return widget

def test_content_select(content_select_window):
    content_select_window.show()

def test_content_select_list_contains_items(content_select_window):
    assert content_select_window.tree.topLevelItemCount() > 0

def test_content_select_select_item(content_select_window):

    item = content_select_window.tree.topLevelItem(0).child(0)
    content_select_window.select_content(item)
