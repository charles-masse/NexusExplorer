
import os

import numpy

from sklearn.neighbors import KDTree
from sklearn.cluster import DBSCAN, AgglomerativeClustering

from PyQt6.QtCore import QCoreApplication

from PIL import Image, ImageOps, ImageFile

from main import settings

# def calculateBounds(bounds0, bounds1, bounds2, bounds3):
#     return int(bounds0) * (32 / MAP_SCALE), int(bounds1) * (32 / MAP_SCALE), int(bounds2) * (32 / MAP_SCALE), int(bounds3) * (32 / MAP_SCALE)

MAP_SIZE = 128
MAP_CHUNK_RESOLUTION = 512
HALF_MAP = int(((MAP_SIZE / 2) * MAP_CHUNK_RESOLUTION))

MAP_SCALE = settings['mapScale']
CLUSTER_DISTANCE = settings['clusterDistance']

def chunkCoords(chunkName):
    """
    Parse the minimap chunk name into map coords
    """
    chunkCoords = chunkName.split('.')[-1]
    xChunk = int(chunkCoords[2:4], 16)
    yChunk = int(chunkCoords[0:2], 16)

    return [xChunk, yChunk]

def locsToPos(locationList):
    """
    Return the position of all locations in the list
    """
    return [(float(location['position0']), float(location['position2'])) for location in locationList]

def worldCoords(posX, posY):
    """
    Map coords to world coords
    """
    return -int(HALF_MAP - (posX * MAP_SCALE)), -int(HALF_MAP - (posY * MAP_SCALE))

def screenPos(worldX, worldY):
    """
    World coords to map coords
    """
    return (HALF_MAP + float(worldX)) / MAP_SCALE, (HALF_MAP + float(worldY)) / MAP_SCALE

class WorldMap:
    """
    Generate the stitched minimap and retain world data
    """
    def __init__(self, world, maxCallback, progressCallback):

        self.world = world

        mapPath = world['assetPath'].replace('\\', '/')
        cachePath = f'./cache/{mapPath}.png'

        if os.path.exists(cachePath):
            self.im = Image.open(cachePath)

        else:
            # Get chunk images
            chunkPath = f'{Settings()['gameFiles']}/{mapPath}'
            chunks = [[chunkName] + chunkCoords(chunkName) for chunkName in os.listdir(chunkPath)]
            # Set the maximum value for the loading bar
            maxCallback(len(chunks))
            QCoreApplication.processEvents()
            # Create Image
            xMax = int((max(chunks, key=lambda x: x[1])[1] * MAP_CHUNK_RESOLUTION) / MAP_SCALE)
            yMax = int((max(chunks, key=lambda x: x[2])[2] * MAP_CHUNK_RESOLUTION) / MAP_SCALE)
            self.im = Image.new('RGB', (xMax, yMax))

            for chunkId, (chunkName, xChunk, yChunk) in enumerate(chunks):
                # Update loading bar
                progressCallback(chunkId)
                QCoreApplication.processEvents()
                # Load chunk
                with Image.open('/'.join([chunkPath, chunkName, chunkName + '.png'])) as imChunk:
                    # Scale map and paste at the right postion
                    imChunk = ImageOps.scale(imChunk, 1 / MAP_SCALE)
                    scaledPos = int(MAP_CHUNK_RESOLUTION / MAP_SCALE)
                    self.im.paste(imChunk, (xChunk * scaledPos, yChunk * scaledPos))
            # Save map for faster loading
            os.makedirs(os.path.dirname(cachePath), exist_ok=True)
            self.im.save(cachePath)

        self.clusterLocations()

    def clusterLocations(self):
        """
        Use sklearn to cluster the different world locations
        """
        self.locations = [loc for loc in self.world['WorldLocation2'].values()]
        # Finding lone locations
        if len(self.locations) > 1:

            findLoners = DBSCAN(eps=CLUSTER_DISTANCE, min_samples=1)
            findLoners.fit_predict(locsToPos(self.locations), sample_weight=[int('QuestHub' in location or 'WorldZone' in location) for location in self.locations])

            loners = [self.locations[i] for i, label in enumerate(findLoners.labels_) if label == -1]

            unnamedHubs = {}
            # Clustering them into unnamed hubs
            if len(loners) > 1:
                clusterLoners = AgglomerativeClustering(n_clusters=None, distance_threshold=CLUSTER_DISTANCE)
                clusterLoners.fit_predict(locsToPos(loners))

                for i, label in enumerate(clusterLoners.labels_):
                    unnamedHubs.setdefault(label, []).append(loners[i])
            # Clustering locations around hubs
            centroids = locsToPos([location for location in self.locations if 'QuestHub' in location or 'WorldZone' in location]) + [numpy.average(locsToPos(hub), axis=0) for hub in unnamedHubs.values()]

            hubClustering = KDTree(centroids)
            labels = hubClustering.query(locsToPos(self.locations), k=1)

            clusters = {}

            for i, label in enumerate(labels[1]):
                clusters.setdefault(label[0], []).append(self.locations[i])
            # Merge clusters with similar names
            clusterByNames = {}

            for i, cluster in enumerate(clusters.values()):

                names = []

                for location in cluster:

                    for name in [name for name in ['QuestHub', 'WorldZone'] if name in location]:
                        names.extend([hub['localizedTextIdName'] for hub in location[name].values()])

                if names:
                    clusterByNames.setdefault(names[0], []).extend(cluster)
                else:
                    clusterByNames.setdefault('Unnamed Location {i}', []).extend(cluster)
            # Merge clusters
            mergedLocations = []

            for cluster in clusterByNames:

                posX, posY = numpy.average(locsToPos(clusterByNames[cluster]), axis=0)

                clusterDict = {'position0':str(posX), 'position2':str(posY), 'clusterName':cluster}

                for location in clusterByNames[cluster]:
                    for key in [key for key in location if type(location[key]) is dict]:

                        clusterDict.setdefault(key, {}).update(location[key])

                mergedLocations.append(clusterDict)

            self.locations = mergedLocations
