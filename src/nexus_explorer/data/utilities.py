
import re
from urllib.parse import quote

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
    'item' : 'Item2',
    'location' : 'WorldLocation2',
    'mission' : 'PathMission',
    'quest' : 'Quest2',
    'schematic' : 'TradeskillSchematic2',
    'vitem' : 'VirtualItem',
}

def link_referenced(loading_manager: LoadingManager, text: str) -> str:
    """Add hypertext to a string."""
    for match in re.finditer(r'(?:<text[^>]*?>)?\$\S*?\((\w+)=(\d+)\)|\$(\w+)=(\d+)(?:</text>)?|<text\s+Link="(\w+):(\d+)">([\s\S]*?)</text>', text):

        full_match = match.group(0)
        link_name = match.group(1) or match.group(3) or match.group(5)
        link_id = match.group(2) or match.group(4) or match.group(6)
        link_text = match.group(7) or None

        db_name = DATABASES[link_name.lower()]

        linked = loading_manager[db_name].get(int(link_id))

        if not link_text:
            
            if linked:
                link_text = linked.get('localizedTextIdName')

            elif not link_text:
                link_text = f"{db_name} id:{link_id} not found"

        text = text.replace(full_match, f'<b><a style="color: rgb(125, 251, 182);" href="{quote(str(linked))}">[{link_text}]</a></b>')

    return text
