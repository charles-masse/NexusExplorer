
class WorldData:

    def __init__(
            self,
            id: int,
            assetPath: str,
            localizedTextIdName: str,
            WorldLocation2: list["LocationData"] | None = None,
            **kargs
        ) -> None:

        self.id = id
        self.name = localizedTextIdName

        self.isMap = False
        self.map_path = assetPath
        self.map_name = assetPath.split('\\')[-1]

        self.locations = WorldLocation2 or []

class LocationData:

    def __init__(
            self,
            position0: float,
            position2: float,
            radius: float = 1,
            worldZoneId: list[dict] | None=None,
            Challenge: list[dict] | None=None,
            Datacube: list[dict] | None=None,
            PublicEvent: list[dict] | None=None,
            PublicEventObjective: list[dict] | None=None,
            Quest2: list[dict] | None=None,
            QuestObjective: list[dict] | None=None,
            QuestHub: list[dict] | None=None,
            PathMission: list[dict] | None=None,
            **kargs
        ):
        
        self.position = [position0, position2]
        self.radius = radius
        #TODO CBB
        if worldZoneId and not isinstance(worldZoneId, int):

            if not isinstance(worldZoneId, list):
                self.zones = [worldZoneId]
            else:
                self.zones = worldZoneId
    
        else:
            self.zones = []

        self.challenges = Challenge or []
        self.datacubes = Datacube or []
        self.events = PublicEvent or []
        self.event_objectives = PublicEventObjective or []
        self.quests = Quest2 or []
        self.quest_objectives = QuestObjective or []
        self.hubs = QuestHub or []
        self.missions = PathMission or []
        #TODO CBB
        for z in self.zones:
            print(z)
            datacubes = z.get('Datacube')
            if datacubes:
                self.datacubes.extend(datacubes)

        self.name = self._get_name()

    def calculate_weight(self) -> float:

        if self.name != '':
            return 1 # * self.radius

        return 0

    def _get_name(self) -> str | None:

        names: list[str|None] = []

        for hub in [h for h in self.hubs if h.get('localizedTextIdName')]:
            names.append(hub.get('localizedTextIdName'))

        for zone in [z for z in self.zones if z.get('localizedTextIdName')]:
            names.append(zone.get('localizedTextIdName'))

        for challenge in [c for c in self.challenges if c.get('location')]:
            names.append(challenge.get('localizedTextIdLocation'))

        if names: #Just take the first in the list--they seem to be similar in most cases or they will be in order of priority (hub, zone, challenge)
            return names[0]

        return ''
