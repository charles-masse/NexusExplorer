
def add_mission_locations(window, mission, label):

    loading_manager = window.loading_manager

    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(mission[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, label)

def get_mission_context(window):
    return window.content, window.loading_manager

def get_target_group(loading_manager, group_id):

    target = loading_manager['TargetGroup'].get(group_id)
    if target:

        creatures = []

        for i in range(7):

            creature = loading_manager['Creature2'].get(target[f'data{i}'])
            if creature:
                creatures.append(f'$(creature={creature['ID']})')

        if len(creatures):
            return " or ".join([", ".join(creatures[:-1]),creatures[-1]])

    return f'<b>[TargetGroup id:{group_id} not found]</b>'
