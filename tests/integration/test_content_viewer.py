
import pytest

from nexus_explorer.ui.content_select import ContentItem  # type: ignore[import-untyped]
from nexus_explorer.ui.content_viewer import (  # type: ignore[import-untyped]
    ContentViewerWindow,
)

def test_content_viewer_window_datacube(loading_manager):

    sample_content = ContentItem(loading_manager, loading_manager['Datacube'].get(1), {'id':0})
    ContentViewerWindow(loading_manager, sample_content, None)


def test_content_viewer_window_quest(loading_manager):

    sample_content = ContentItem(loading_manager, loading_manager['Quest2'].get(1), {'id':1})
    ContentViewerWindow(loading_manager, sample_content, None)

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
    loading_manager,
    path_type,
    mission_id,
):

    sample_content = ContentItem(
        loading_manager,
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

    ContentViewerWindow(loading_manager, sample_content, None)

def test_content_viewer_window_unknown_mission(loading_manager):

    sample_content = ContentItem(
        loading_manager,
        {
            'pathTypeEnum': 9,
            'pathMissionTypeEnum': 99,
        }, 
        {'id': 2}
    )

    with pytest.raises(TypeError):
        ContentViewerWindow(loading_manager, sample_content, None)

def test_content_viewer_window_event(loading_manager):

    sample_content = ContentItem(loading_manager, loading_manager['PublicEvent'].get(1), {'id':3})
    ContentViewerWindow(loading_manager, sample_content, None)

def test_content_viewer_window_challenge(loading_manager):

    sample_content = ContentItem(loading_manager, loading_manager['Challenge'].get(1), {'id':4})
    ContentViewerWindow(loading_manager, sample_content, None)

def test_content_viewer_window_unknown_content(loading_manager):

    sample_content = ContentItem(loading_manager, loading_manager['World'].get(1), {'id':42})
    with pytest.raises(TypeError):
        ContentViewerWindow(loading_manager, sample_content, None)

def test_content_viewer_window_close(loading_manager, qtbot):

    sample_content = ContentItem(loading_manager, loading_manager['Challenge'].get(1), {'id':4})

    widget = ContentViewerWindow(loading_manager, sample_content, None)
    qtbot.addWidget(widget)

    widget.show()
    widget.close()
