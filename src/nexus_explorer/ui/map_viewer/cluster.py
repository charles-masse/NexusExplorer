
import numpy
from sklearn.cluster import DBSCAN  # type: ignore[import-untyped]
from sklearn.neighbors import KDTree  # type: ignore[import-untyped]

CLUSTER_DISTANCE = 128

def merge_locations(locations):

    radius = [loc.radius for loc in locations]

    merged_location = LocationData(0, 0, radius)
    #TODO fix this
    merged_location.position = []
    for loc in locations:
        merged_location.position.extend(loc.position)

        for content_key in loc.contents:

            contents = loc.contents[content_key]

            if isinstance(contents, list):
                merged_location.contents.setdefault(content_key, []).extend(contents)

    return merged_location

class LocationData:

    def __init__(
            self,
            position0: float,
            position2: float,
            radius: float = 1,
            **kwargs
        ):
        
        self.position = [[position0, position2]]
        self.radius = [radius]
        self.contents = kwargs

        self.name = self._get_name()

    def calculate_weight(self) -> float:

        if self.name != '':
            return self.get_radius()

        return 0

    def _get_name(self) -> str:

        names: list[str] = []

        for hub in [h for h in self.contents.get('QuestHub', []) if h.get('localizedTextIdName')]:
            names.append(hub.get('localizedTextIdName'))

        for zone in [z for z in self.contents.get('WorldZone', []) if z.get('localizedTextIdName')]:
            names.append(zone.get('localizedTextIdName'))

        for challenge in [c for c in self.contents.get('Challenge', []) if c.get('localizedTextIdLocation')]:
            names.append(challenge.get('localizedTextIdLocation'))

        if names: #Just take the first in the list--they seem to be similar in most cases or they will be in order of priority (hub, challenge)
            return names[0]

        return ''

    def get_position(self):
        return numpy.median(self.position, axis=0)

    def get_radius(self):
        return max(self.radius)


def cluster_locations(locations: list[LocationData]) -> list[LocationData]:
    """Use sklearn to cluster the different world locations""" #TODO clean up
    #Separate locations by name
    location_names: dict[str, list[LocationData]] = {}

    for loc in locations:
        location_names.setdefault(loc._get_name(), []).append(loc)
    #Merge locations with the same name into one LocationData
    merged_locs = []

    for name, loc_list in location_names.items():

        if name == '' or len(loc_list) == 1:
            merged_locs.extend(loc_list)

        else:
            merged_loc = merge_locations(loc_list)
            merged_locs.append(merged_loc)
    #DBSCAN Clustering locations around locations with named hubs/zones/named challenge
    dbscan = DBSCAN(eps=CLUSTER_DISTANCE, min_samples=1)
    dbscan.fit([loc.get_position() for loc in merged_locs], sample_weight=[loc.calculate_weight() for loc in merged_locs])
    #Clustering lone locations into unnamed cluster
    unnamed_locations: dict[int, list[LocationData]] = {}
    
    lone_locs = [merged_locs[label_id] for label_id, label in enumerate(dbscan.labels_) if label == -1]

    if len(lone_locs):
        dbscan.fit([loc.get_position() for loc in lone_locs])

        for label_id, label in enumerate(dbscan.labels_):
            unnamed_locations.setdefault(label, []).append(lone_locs[label_id])
    #Get named hubs/zones/challenge location
    named_locations = [loc for loc in merged_locs if loc.name != '']
    #Combine unnamed and named clusters' position
    centroids = [numpy.average([loc.get_position() for loc in locs], axis=0) for locs in unnamed_locations.values()] + [loc.get_position() for loc in named_locations]
    #Cluster locations to closest hub using KdTree
    kdtree = KDTree(centroids)
    kdtree_results = kdtree.query([loc.get_position() for loc in merged_locs], k=1)
    #Merge clusters into 1 LocationData
    final_clusters: dict[int, list[LocationData]] = {}
    #Go through all the labels
    for label_id, label in enumerate(kdtree_results[1]):
        final_clusters.setdefault(label[0], []).append(merged_locs[label_id])

    final_locations = []

    for cluster in final_clusters.values():
        merged_loc = merge_locations(cluster)
        final_locations.append(merged_loc)
    #Sort for icon layering
    final_locations.sort(key=lambda index: index.get_position()[1])

    return final_locations
