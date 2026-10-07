
from nexus_explorer.data import LoadingManager
from nexus_explorer.ui import (
    ContentSelectWindow,
    ContentViewerWindow,
    MapViewer,
    WorldSelectWindow,
)
from nexus_explorer.ui.map_viewer.cluster import LocationData
from nexus_explorer.ui.map_viewer.objects import LocationObject
from nexus_explorer.ui.map_viewer.window import MapScene
from nexus_explorer.ui.world_select.utilities import WorldData

loading_manager = LoadingManager('tests/sample_data')

def test_world_select(qtbot):

    widget = WorldSelectWindow(loading_manager)
    qtbot.addWidget(widget)

    widget.load_world_button.click()

def test_map_scene(qtbot):

    widget = MapViewer(loading_manager, WorldData('0', '', 'TestWorld'))
    qtbot.addWidget(widget)

def test_content_select(qtbot):
    
    scene = MapScene(loading_manager, WorldData('0', '', 'TestWorld'))
    icon = LocationObject(LocationData(0, 0), scene)

    widget = ContentSelectWindow(loading_manager, icon)
    qtbot.addWidget(widget)

# def test_content_viewer(qtbot):

#     widget = ContentViewerWindow(loading_manager, 'Datacube', None)
#     qtbot.addWidget(widget)
