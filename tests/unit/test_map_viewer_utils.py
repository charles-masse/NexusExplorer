
import pytest

from nexus_explorer.ui.map_viewer.cluster import (  # type: ignore[import-untyped]
    LocationData,
    cluster_locations,
    merge_locations,
)


@pytest.fixture
def locations(loading_manager):
    return [LocationData(**location) for location in loading_manager['WorldLocation2'].values()]

def test_merge_locations(locations):
    assert merge_locations(locations)

def test_cluster_locations(locations):
    
    clustered_locs = cluster_locations(locations)

    assert len(clustered_locs) < len(locations)
