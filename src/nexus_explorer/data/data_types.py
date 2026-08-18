
class WorldData:

    def __init__(self, itemId, assetPath, name, WorldLocation2=None, **kargs): #chunkBounds00, chunkBounds01, chunkBounds02, chunkBounds03,

        self.id = itemId
        self.name = name

        self.isMap = False
        self.map_path = assetPath
        self.map_name = assetPath.split('\\')[-1]

        self.locations = WorldLocation2 or []

    def cleanup_locations(self):
        #TODO CBB
        new_list = []

        for location in self.locations:
            new_list.append(LocationData(**location))

        self.locations = new_list

class LocationData:

    def __init__(self, radius, position0, position2, WorldZone=None, Challenge=None, Datacube=None, PublicEvent=None, Quest2=None, QuestHub=None, PathMission=None, **kargs): # worldId, worldZoneId, itemId,
        
        self.position = [float(position0), float(position2)]
        self.radius = radius

        # self.worldZoneId = worldZoneId #TODO Make sure we're not losing zones because they're not linking back to their location

        self.zones = WorldZone or []
        self.challenges = Challenge or []
        self.datacubes = Datacube or []
        self.events = PublicEvent or []
        self.quests = Quest2 or []
        self.hubs = QuestHub or []
        self.missions = PathMission or []

        self.name = self._get_name()

    def calculate_weight(self):

        if self.name != '':
            return 1 * self.radius #TODO testing with radius scaling

        return 0

    def _get_name(self):

        names = []

        for hub in [h for h in self.hubs if h.get('name')]:
            names.append(hub.get('name'))

        for zone in [z for z in self.zones if z.get('name')]:
            names.append(zone.get('name'))

        for challenge in [c for c in self.challenges if c.get('location')]:
            names.append(challenge.get('location'))

        if names: #Just take the first in the list--they seem to be similar in most cases or they will be in order of priority (hub, zone, challenge)
            return names[0]

        return ''
