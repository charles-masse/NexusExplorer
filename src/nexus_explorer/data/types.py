
class WorldData:

    def __init__(
            self,
            ID: int,
            assetPath: str,
            localizedTextIdName: str,
            WorldLocation2: list["LocationData"] | None = None,
            **kargs
        ) -> None:

        self.id = ID
        self.name = localizedTextIdName
        self.locations = WorldLocation2 or []

        self.isMap = False
        self.map_path = assetPath
        self.map_name = assetPath.split('\\')[-1]

        self.zones = {}

        self.expose_zones()

    def expose_zones(self):

        for location in self.locations:
            self.zones.setdefault(location['worldZoneId'], []).append(LocationData(**location))
                
class LocationData:

    def __init__(
            self,
            position0: float,
            position2: float,
            radius: float = 1,
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
        self.challenges = Challenge or []
        self.datacubes = Datacube or []
        self.events = PublicEvent or []
        self.event_objectives = PublicEventObjective or []
        self.quests = Quest2 or []
        self.quest_objectives = QuestObjective or []
        self.hubs = QuestHub or []
        self.missions = PathMission or []

        self.name = self._get_name()

    def calculate_weight(self) -> float:

        if self.name != '':
            return self.radius

        return 0

    def _get_name(self) -> str | None:

        names: list[str|None] = []

        for hub in [h for h in self.hubs if h.get('localizedTextIdName')]:
            names.append(hub.get('localizedTextIdName'))

        for challenge in [c for c in self.challenges if c.get('location')]:
            names.append(challenge.get('localizedTextIdLocation'))

        if names: #Just take the first in the list--they seem to be similar in most cases or they will be in order of priority (hub, challenge)
            return names[0]

        return ''
