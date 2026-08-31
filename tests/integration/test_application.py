
from nexus_explorer.data import LoadingManager, prep_worlds
from nexus_explorer.ui import WorldSelectWindow
from nexus_explorer.ui.map_viewer import LocationObject


def test_kitchen_sink(qtbot):

    loading_manager = LoadingManager('tests/sample_data')
    prep_worlds(loading_manager)

    widget = WorldSelectWindow(loading_manager)
    qtbot.addWidget(widget)
    #World Select
    world_list = widget.world_list
    world_list.setCurrentRow(0)
    widget.load_world_button.click()
    #Map Viewer
    map_viewer = widget.popup.map_scene

    for loc in [l for l in map_viewer.items() if isinstance(l, LocationObject)]:

        loc.clicked.emit(loc)
        #Content Select
        content_select = map_viewer.popup
        content_list = content_select.tree

        for column in range(content_list.columnCount()):

            header = content_list.itemAt(column, 0)

            for child_id in range(header.childCount()):

                content_item = header.child(child_id)
                content_select.select_content(content_item)
                content_select.popup.close()

        content_select.close()
    #Close everything
    widget.close()
