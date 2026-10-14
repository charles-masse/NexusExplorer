
import pytest
from PyQt6.QtCore import QPoint, Qt

from nexus_explorer.data import LoadingManager  # type: ignore[import-untyped]
from nexus_explorer.ui import MapViewer  # type: ignore[import-untyped]
from nexus_explorer.ui.map_viewer.cluster import (  # type: ignore[import-untyped]
    LocationData,
    cluster_locations,
    merge_locations,
)
from nexus_explorer.ui.map_viewer.generate import (  # type: ignore[import-untyped]
    generate_map,
)
from nexus_explorer.ui.world_select.utilities import (  # type: ignore[import-untyped]
    prep_worlds,
)


#Map Generation
@pytest.fixture
def loading_manager():
    return LoadingManager('tests/sample_data')

@pytest.fixture
def locations(loading_manager):
    return [LocationData(**location) for location in loading_manager['WorldLocation2'].values()]

@pytest.fixture(scope="module")
def map_cache(tmp_path_factory):
    return tmp_path_factory.mktemp(".cache")

def test_generate_map(map_cache):
    map_im = generate_map('tests/sample_data/Map/SampleWorld', map_cache)

    assert len(set(map_im.getdata())) > 1

def test_generate_map_cached(map_cache):
    map_im = generate_map('tests/sample_data/Map/SampleWorld', map_cache)

    assert len(set(map_im.getdata())) > 1
#Location utils
def test_merge_locations(locations):
    assert merge_locations(locations)

def test_cluster_locations(locations):
    clustered_locs = cluster_locations(locations)

    assert len(clustered_locs) < len(locations)
#UI
@pytest.fixture
def map_viewer_window(loading_manager, qtbot):
    worlds = prep_worlds(loading_manager)
    #Find world with map
    for world in worlds:
        if world.map:
            break

    widget = MapViewer(loading_manager, world)
    qtbot.addWidget(widget)

    return widget

def test_map_viewer_window(map_viewer_window):
    map_viewer_window.show()

def test_map_viewer_displays_objects(map_viewer_window):
    assert len(map_viewer_window.map_scene.items()) > 0

@pytest.fixture
def map_view(map_viewer_window, qtbot):
    
    map_viewer_window.show()
    qtbot.waitExposed(map_viewer_window)

    viewport = map_viewer_window.viewport()

    return viewport

def test_map_viewer_mouse_move(map_view, qtbot):
    qtbot.wait(100)
    qtbot.mouseMove(map_view, map_view.rect().center(), 100)
    qtbot.wait(100)
    qtbot.mouseMove(map_view, map_view.rect().center() + QPoint(5, 5), 100)
    qtbot.wait(100)
    
def test_map_viewer_mouse_click(map_view, qtbot):
    qtbot.mouseClick(map_view, Qt.MouseButton.LeftButton)

def test_map_viewer_select_location(map_viewer_window):

    loc = map_viewer_window.map_scene.items()[1]
    map_viewer_window.map_scene.select_object(loc)

    assert map_viewer_window.map_scene.popup

def test_map_viewer_focus_location(map_viewer_window):

    loc = map_viewer_window.map_scene.items()[0]
    map_viewer_window.map_scene.focus(loc)
