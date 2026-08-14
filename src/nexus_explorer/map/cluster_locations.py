
import numpy
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KDTree

from ..data import LocationData

CLUSTER_DISTANCE = 128

def merge_locations(locations):
    #Grab the biggest radius and the median position
    radius = max([loc.radius for loc in locations])
    x, y = numpy.median([loc.position for loc in locations], axis=0)

    return LocationData(
        radius,
        x,
        y,
        [zone for loc in locations for zone in loc.zones],
        [challenge for loc in locations for challenge in loc.challenges],
        [datacube for loc in locations for datacube in loc.datacubes],
        [event for loc in locations for event in loc.events],
        [quest for loc in locations for quest in loc.quests],
        [hub for loc in locations for hub in loc.hubs],
        [mission for loc in locations for mission in loc.missions]
    )

def cluster_locations(locations):
    """
    Use sklearn to cluster the different world locations
    """
    if len(locations) == 0:
        return []
    
    #Merge locations with the same name together
    duplicate_names = {}

    for loc in locations:
        duplicate_names.setdefault(loc.name, []).append(loc)
    
    merged_locs = []

    for name, loc_list in duplicate_names.items():

        if name == '' or len(loc_list) == 1:
            merged_locs.extend(loc_list)

        else:
            merged_loc = merge_locations(loc_list)
            merged_locs.append(merged_loc)
    #DBSCAN setup
    dbscan = DBSCAN(eps=CLUSTER_DISTANCE, min_samples=1)
    #Clustering locations around locations with named hubs/zones/named challenge
    dbscan.fit([loc.position for loc in merged_locs], sample_weight=[loc.calculate_weight() for loc in merged_locs])
    #Clustering lone locations into unnamed cluster
    unnamed_locations = {}
    
    lone_locs = [merged_locs[label_id] for label_id, label in enumerate(dbscan.labels_) if label == -1]

    if len(lone_locs):
        dbscan.fit([loc.position for loc in lone_locs])

        for label_id, label in enumerate(dbscan.labels_):
            unnamed_locations.setdefault(label, []).append(lone_locs[label_id])
    #Get named hubs/zones/challenge location
    named_locations = [loc for loc in merged_locs if loc.name != '']
    #Combine unnamed and named clusters' position
    centroids = [numpy.average([loc.position for loc in locs], axis=0) for locs in unnamed_locations.values()] + [loc.position for loc in named_locations]
    #Cluster locations to closest hub using KdTree
    kdtree = KDTree(centroids)
    kdtree_results = kdtree.query([loc.position for loc in merged_locs], k=1)
    #Merge clusters into 1 LocationData
    final_clusters = {}
    #Go through all the labels
    for label_id, label in enumerate(kdtree_results[1]):
        final_clusters.setdefault(label[0], []).append(merged_locs[label_id])

    final_locations = []

    for cluster in final_clusters.values():
        merged_loc = merge_locations(cluster)
        final_locations.append(merged_loc)
    #Sort for icon layering
    final_locations.sort(key=lambda index: float(index.position[1]))

    return final_locations
