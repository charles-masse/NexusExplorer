
from nexus_explorer.data.utilities import (  # type: ignore[import-untyped]
    link_data,
    link_referenced,
)


def test_loading_data_from_db(loading_manager):
    assert len(loading_manager._loaded)

def test_link_databases(loading_manager):

    link_data(loading_manager, 'WorldZone', 'worldZoneId', ['Datacube'])

    assert [world_zone.get('Datacube') for world_zone in loading_manager['WorldZone'].values()]

def test_link_referenced(loading_manager):
    link_referenced(loading_manager, "$(creature=1)")

def test_link_referenced_no_hyperlink(loading_manager):
    link_referenced(loading_manager, "$(creature=1)", False)
