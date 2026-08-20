
from nexus_explorer.data.data_types import LocationData, WorldData
from nexus_explorer.data.load_data import DBDict, LoadingManager
from nexus_explorer.ui import (
    ContentSelectWindow,
    ContentViewerWindow,
    LocationIcon,
    MapViewerWindow,
    WorldSelectWindow,
)
from nexus_explorer.ui.map_viewer.map_viewer import MapScene

loading_manager = LoadingManager('tests/sample_data')

def test_world_select(qtbot):

    widget = WorldSelectWindow(loading_manager)
    qtbot.addWidget(widget)

    # widget.load_world_button.click()

def test_map_viewer(qtbot):

    widget = MapViewerWindow(loading_manager, WorldData('0', '', 'TestWorld'))
    qtbot.addWidget(widget)

def test_content_select(qtbot):
    
    scene = MapScene(loading_manager, WorldData('0', '', 'TestWorld'))
    icon = LocationIcon(LocationData(0, 0), scene)

    widget = ContentSelectWindow(loading_manager, icon)
    qtbot.addWidget(widget)

def test_content_viewer(qtbot):

    widget = ContentViewerWindow(loading_manager, DBDict('Datacube'))
    qtbot.addWidget(widget)
