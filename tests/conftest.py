import pytest

from nexus_explorer.data import LoadingManager  # type: ignore[import-untyped]
from nexus_explorer.ui.world_select.utilities import (  # type: ignore[import-untyped]
    prep_worlds,
)


@pytest.fixture
def loading_manager():
    manager = LoadingManager("tests/sample_data")
    prep_worlds(manager)
    
    return manager
