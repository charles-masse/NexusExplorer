
import pytest

from nexus_explorer.data import LoadingManager  # type: ignore[import-untyped]
from nexus_explorer.ui import WorldSelectWindow  # type: ignore[import-untyped]
from nexus_explorer.ui.world_select.utilities import (  # type: ignore[import-untyped]
    prep_worlds,
)


@pytest.fixture
def loading_manager():
    return LoadingManager('tests/sample_data')
#Utilities
def test_prep_worlds(loading_manager):
    worlds = prep_worlds(loading_manager)
    assert len(worlds)
#UI
@pytest.fixture
def world_select_window(loading_manager, qtbot):

    widget = WorldSelectWindow(loading_manager)
    qtbot.addWidget(widget)

    return widget

def test_world_select_window(world_select_window):
    world_select_window.show()

def test_world_select_list_contains_worlds(world_select_window):
    assert world_select_window.world_list.count() > 0

def test_world_select_load_world_button(qtbot, world_select_window):

    world_select_window.world_list.setCurrentRow(0)
    world_select_window.load_world_button.click()

    assert world_select_window.popup
    qtbot.addWidget(world_select_window.popup)
