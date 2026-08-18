
from nexus_explorer.map.cluster_locations import cluster_locations, merge_locations
from nexus_explorer.map.generate_map import generate_map

from ..sample_data import sample_location0, sample_location1


def test_generate_map():
    map_im = generate_map('tests/sample_data/Map/SampleWorld', False)
    map_data = list(set(map_im.getdata()))

    assert len(map_data) > 1

def test_merge_locations():
    merge_locations([sample_location0, sample_location1])

    #TODO

def test_cluster_no_locations():
    clustered_locs = cluster_locations([])

    assert len(clustered_locs) == 0

def test_cluster_locations():
    clustered_locs = cluster_locations([sample_location0, sample_location1])

    assert len(clustered_locs) == 1
