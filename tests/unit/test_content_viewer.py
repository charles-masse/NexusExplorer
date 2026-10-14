
import pytest

from nexus_explorer.data import LoadingManager  # type: ignore[import-untyped]
from nexus_explorer.ui.content_select import ContentItem  # type: ignore[import-untyped]
from nexus_explorer.ui.content_viewer import (  # type: ignore[import-untyped]
    ContentViewerWindow,
)
from nexus_explorer.ui.world_select.utilities import (  # type: ignore[import-untyped]
    prep_worlds,
)


@pytest.fixture
def loading_manager():

    manager = LoadingManager('tests/sample_data')
    prep_worlds(manager)

    return manager

def test_content_viewer_window_datacube(loading_manager, qtbot):

    sample_content = ContentItem(loading_manager, loading_manager['Datacube'].get(1), {'id':0})

    widget = ContentViewerWindow(loading_manager, sample_content, None)
    qtbot.addWidget(widget)

    widget.show()

def test_content_viewer_window_quest(loading_manager, qtbot):

    sample_content = ContentItem(loading_manager, loading_manager['Quest2'].get(1), {'id':1})

    widget = ContentViewerWindow(loading_manager, sample_content, None)
    qtbot.addWidget(widget)

    widget.show()

def test_content_viewer_window_event(loading_manager, qtbot):

    sample_content = ContentItem(loading_manager, loading_manager['PublicEvent'].get(1), {'id':3})

    widget = ContentViewerWindow(loading_manager, sample_content, None)
    qtbot.addWidget(widget)

    widget.show()

def test_content_viewer_window_challenge(loading_manager, qtbot):

    sample_content = ContentItem(loading_manager, loading_manager['Challenge'].get(1), {'id':4})

    widget = ContentViewerWindow(loading_manager, sample_content, None)
    qtbot.addWidget(widget)

    widget.show()

def test_content_viewer_window_close(loading_manager, qtbot):

    sample_content = ContentItem(loading_manager, loading_manager['Challenge'].get(1), {'id':4})

    widget = ContentViewerWindow(loading_manager, sample_content, None)
    qtbot.addWidget(widget)

    widget.show()
    widget.close()
