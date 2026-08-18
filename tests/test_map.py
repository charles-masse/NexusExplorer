
# import pytest

from nexus_explorer.data.data_types import LocationData
from nexus_explorer.map.cluster_locations import cluster_locations, merge_locations

sample_location0 = LocationData(**{'ID':'0', 'radius':'1', 'maxVerticalDistance':'0', 'position0':'0', 'position1':'0', 'position2':'0', 'facing0':'0', 'facing1':'0', 'facing2':'0', 'facing3':'1', 'worldId':'42', 'worldZoneId':'123', 'phases':'1'})
sample_location1 = LocationData(**{'ID':'1', 'radius':'99', 'maxVerticalDistance':'0', 'position0':'50', 'position1':'0', 'position2':'50', 'facing0':'0', 'facing1':'0', 'facing2':'0', 'facing3':'1', 'worldId':'42', 'worldZoneId':'456', 'phases':'-1'})

def test_merge_locations():
    merge_locations([sample_location0, sample_location1])

def test_cluster_no_locations():
    
    clustered = cluster_locations([])

    assert len(clustered) == 0

def test_cluster_locations():

    clustered = cluster_locations([sample_location0, sample_location1])

    assert len(clustered) == 1
