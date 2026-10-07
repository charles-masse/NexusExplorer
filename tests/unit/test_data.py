
from nexus_explorer.data import LoadingManager
from nexus_explorer.data.utilities import link_data

loading_manager = LoadingManager('tests/sample_data')

def test_loading_data_from_db():
    
    data = loading_manager['World']

    assert len(data)

def test_link_databases():

    link_data(loading_manager, 'WorldZone', 'worldZoneId', ['Datacube'])

    assert [world_zone.get('Datacube') for world_zone in loading_manager['WorldZone'].values()]
