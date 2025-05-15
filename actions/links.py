
import re

from singletons import LocalizedStrings, loadManager

TEST = {
        'creature' : 'Creature2',
        'vitem' : 'VirtualItem',
        'item' : 'Item2',
        'schematic' : 'TradeskillSchematic2'
       }

def linkGameObject(text):

    for match in re.finditer(r'(?:<text[^>]*?>)?\$\S*?\((\w+)=(\d+)\)|\$(\w+)=(\d+)(?:</text>)?', text):

        fullMath = match.group(0)
        key = match.group(1) or match.group(3)
        idValue = match.group(2) or match.group(4)

        linked = loadManager[TEST[key.lower()]].get(idValue)

        if linked:
            linkedText = LocalizedStrings[linked.get('localizedTextIdName')]
            
        else:
            linkedText = None

        if not linkedText:
            linkedText = f"Can't find {key}:{idValue}"

        text = text.replace(fullMath, f'<b><a style="color: rgb(125, 251, 182); text-decoration: none;" href="{linked}">[{linkedText}]</a></b>')

    return text
