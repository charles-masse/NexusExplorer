
from nexus_explorer.data.load_data import DBDict, LoadingManager
from nexus_explorer.data.parse_data import link_data


def test_loading_data_from_db():
    
    loading_manager = LoadingManager('tests/sample_data')
    data = loading_manager['World']

    assert len(data)

def test_link_databases():

    targetDb = DBDict('target', {'0':{'foo':'123'}})
    sourceDb = DBDict('source', {'0':{'bar':'0'}})

    linked = link_data(targetDb, 'bar', [sourceDb])

    assert linked['0'].get('source') != None
