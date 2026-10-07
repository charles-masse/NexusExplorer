
import re

from . import LoadingManager


def link_data(loading_manager: LoadingManager, target:str, field_name:str, source:list[str]):
    """Link data that referenced the target
    - loading_manager: The loading manager that contains the databases.
    - target: The database referenced and that will be returned.
    - field_name: Name of the field that contains the reference ids (in targetDb).
    - source: A list of databases that contains a reference to the target.
    """
    for db in source:
        for item in loading_manager[db].values():
            for key in [k for k in item if field_name.lower() in k.lower()]:
                #Add item that referenced this data
                linked_item = loading_manager[target].get(item[key])
                if linked_item:
                    linked_item.setdefault(db, []).append(item)

DATABASES = {
    'creature' : 'Creature2',
    'vitem' : 'VirtualItem',
    'item' : 'Item2',
    'schematic' : 'TradeskillSchematic2',
    'quest' : 'Quest2'
}

def link_referenced(loading_manager: LoadingManager, text: str, hyperlink: bool = True) -> str:
    """Add hypertext to a string.""" #TODO plural vs singular item
    regex = re.finditer(r'(?:<text[^>]*?>)?\$\S*?\((\w+)=(\d+)\)|\$(\w+)=(\d+)(?:</text>)?', text)
    for match in regex:

        full_match = match.group(0)
        db_name = match.group(1) or match.group(3)
        db_id = match.group(2) or match.group(4)

        linked = loading_manager[DATABASES[db_name.lower()]].get(int(db_id))

        if linked:
            linked_text = linked.get('localizedTextIdName')

        if not linked or not linked_text:
            linked_text = f"{db_name} id:{db_id} not found"

        if hyperlink: #TODO CBB
            text = text.replace(full_match, f'<b><a style="color: rgb(125, 251, 182);" href="{linked}">[{linked_text}]</a></b>')
        else:
            text = text.replace(full_match, f'[{linked_text}]')

    return text

def replace_data(loading_manager: LoadingManager, target: str, field_name: str, source: str):
    """Replace data that referenced the target with the actual data.
    - loading_manager: The loading manager that contains the databases.
    - target: The database referenced and that will be returned.
    - field_name: Name of the field that contains the reference ids (in targetDb).
    - source: The database that contains a reference to the target.
    """
    for item in loading_manager[target].values():
        for key in [k for k in item if field_name.lower() in k.lower()]:
            replacement_item = loading_manager[source].get(item[key])
            if replacement_item:
                item[key] = replacement_item
