
import pytest

from nexus_explorer.data import LoadingManager  # type: ignore[import-untyped]
from nexus_explorer.ui import MapViewer  # type: ignore[import-untyped]
from nexus_explorer.ui.content_select import ContentItem  # type: ignore[import-untyped]
from nexus_explorer.ui.content_viewer import (  # type: ignore[import-untyped]
    ContentViewerWindow,
)
from nexus_explorer.ui.world_select.utilities import (  # type: ignore[import-untyped]
    prep_worlds,
)


@pytest.fixture
def loading_manager_override():
    manager = LoadingManager("tests/sample_data")
    
    return manager

@pytest.fixture
def map_object(loading_manager_override):

    worlds = prep_worlds(loading_manager_override)

    viewer = MapViewer(loading_manager_override, worlds[1])
    obj = viewer.map_scene.items()[1]

    return obj

@pytest.mark.parametrize('content_id', range(1, 51))
def test_content_viewer_window_datacube(loading_manager_override, content_id, map_object):

    sample_content = ContentItem(loading_manager_override, loading_manager_override['Datacube'].get(content_id), {'id':0})
    ContentViewerWindow(loading_manager_override, sample_content, map_object)

@pytest.mark.parametrize('content_id', range(1, 51))
def test_content_viewer_window_quest(loading_manager_override, content_id, map_object):

    sample_content = ContentItem(loading_manager_override, loading_manager_override['Quest2'].get(content_id), {'id':1})
    ContentViewerWindow(loading_manager_override, sample_content, map_object)

"""pathTypeEnum
0 - Soldier
1 - Settler
2 - Scientist
3 - Explorer
"""
@pytest.mark.parametrize(
    ('path_type', 'mission_id'),
    [
        (0, 0),  # Soldier security
        (2, 2),  # Scientist analysis
        (3, 3),  # Explorer stalking
        (0, 4),  # Soldier assassinate
        (0, 5),  # Soldier demolition
        (0, 6),  # Soldier rescue
        (0, 7),  # Soldier SWAT
        (3, 12),  # Explorer exploration
        (3, 13),  # Explorer scavenger
        (2, 14),  # Scientist analysis
        (3, 15),  # Explorer vista
        (3, 16),  # Explorer cartography
        (3, 17),  # Explorer operation 
        (3, 18),  # Explorer scavenger
        (1, 19),  # Settler expansion
        (2, 20),  # Scientist study
        (1, 21),  # Settler project
        (2, 22),  # Scientist experimentation
        (2, 23),  # Scientist specimen survey
        (2, 24),  # Scientist datacube
        (1, 25),  # Settler service
        (1, 26),  # Settler safety
        (1, 27),  # Settler cache
    ],
)

def test_content_viewer_window_mission_types(
    loading_manager_override,
    map_object,
    path_type,
    mission_id,
):

    sample_content = ContentItem(
        loading_manager_override,
        {
            'objectId': 1,
            'pathTypeEnum': path_type,
            'pathMissionTypeEnum': mission_id,
            'localizedTextIdUnlock': 'Lorem Ipsum',
            'localizedTextIdSoldierOrders': 'Lorem Ipsum, maggot!',
            'localizedTextIdCommunicator': 'Lorem Ipsum',
        }, 
        {'id': 2}
    )

    ContentViewerWindow(loading_manager_override, sample_content, map_object)

def test_content_viewer_window_unknown_mission(loading_manager_override, map_object):

    sample_content = ContentItem(
        loading_manager_override,
        {
            'pathTypeEnum': 9,
            'pathMissionTypeEnum': 99,
        }, 
        {'id': 2}
    )

    with pytest.raises(TypeError):
        ContentViewerWindow(loading_manager_override, sample_content, map_object)

@pytest.mark.parametrize('content_id', range(1, 51))
def test_content_viewer_window_event(loading_manager_override, content_id, map_object):

    sample_content = ContentItem(loading_manager_override, loading_manager_override['PublicEvent'].get(content_id), {'id':3})
    ContentViewerWindow(loading_manager_override, sample_content, map_object)

@pytest.mark.parametrize('content_id', range(1, 51))
def test_content_viewer_window_challenge(loading_manager_override, content_id, map_object):

    sample_content = ContentItem(loading_manager_override, loading_manager_override['Challenge'].get(content_id), {'id':4})
    ContentViewerWindow(loading_manager_override, sample_content, map_object)

def test_content_viewer_window_unknown_content(loading_manager_override, map_object):

    sample_content = ContentItem(loading_manager_override, loading_manager_override['Challenge'].get(1) , {'id':42})
    with pytest.raises(TypeError):
        ContentViewerWindow(loading_manager_override, sample_content, map_object)

def test_content_viewer_window_close(loading_manager_override, map_object, qtbot):

    sample_content = ContentItem(loading_manager_override, loading_manager_override['Challenge'].get(1), {'id':4})

    widget = ContentViewerWindow(loading_manager_override, sample_content, map_object)
    qtbot.addWidget(widget)

    widget.show()
    widget.close()
