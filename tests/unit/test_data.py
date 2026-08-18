
from nexus_explorer.data.load_data import LoadingManager


def test_loading_data_from_db():
    loading_manager = LoadingManager('tests/sample_data')
    data = loading_manager['SampleDatabase']

    assert len(data)
