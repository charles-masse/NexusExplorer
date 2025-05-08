
import os

import numpy

from PyQt6.QtCore import QCoreApplication

from sklearn.neighbors import KDTree
from sklearn.cluster import DBSCAN, AgglomerativeClustering

from PIL import Image, ImageOps

from singletons import settings, LocalizedStrings

MAP_SIZE = 128
MAP_CHUNK_RESOLUTION = 512

def chunkCoords(chunkName):
    """
    Parse the minimap chunk name into map coords
    """
    chunkCoords = chunkName.split('.')[-1]
    xChunk = int(chunkCoords[2:4], 16)
    yChunk = int(chunkCoords[0:2], 16)

    return [xChunk, yChunk]

def generateMapImage(world, maxCallback, progressCallback):

    mapPath = world['assetPath'].replace('\\', '/')
    cachePath = f'./cache/{mapPath}.png'

    if os.path.exists(cachePath):
        im = Image.open(cachePath)

    else:
        # Get chunk images
        chunkPath = f'{settings['gameFiles']}/{mapPath}'
        chunks = [[chunkName] + chunkCoords(chunkName) for chunkName in os.listdir(chunkPath)]
        # Set the maximum value for the loading bar
        maxCallback(len(chunks))
        QCoreApplication.processEvents()
        # Create Image
        xMax = int((max(chunks, key=lambda x: x[1])[1] * MAP_CHUNK_RESOLUTION) / settings['mapScale'])
        yMax = int((max(chunks, key=lambda x: x[2])[2] * MAP_CHUNK_RESOLUTION) / settings['mapScale'])

        im = Image.new('RGB', (xMax, yMax))

        for chunkId, (chunkName, xChunk, yChunk) in enumerate(chunks):
            # Update loading bar
            progressCallback(chunkId)
            QCoreApplication.processEvents()
            # Load chunk
            with Image.open('/'.join([chunkPath, chunkName, chunkName + '.png'])) as imChunk:
                # Scale map and paste at the right postion
                imChunk = ImageOps.scale(imChunk, 1 / settings['mapScale'])
                scaledPos = int(MAP_CHUNK_RESOLUTION / settings['mapScale'])
                im.paste(imChunk, (xChunk * scaledPos, yChunk * scaledPos))
        # Save map for faster loading
        os.makedirs(os.path.dirname(cachePath), exist_ok=True)
        im.save(cachePath)

    return im

def locsToPos(locationList):
    """
    Return the position of all locations in the list
    """
    return [(float(location['position0']), float(location['position2'])) for location in locationList]

def clusterLocations(locations):
    """
    Use sklearn to cluster the different world locations
    """
    locationList = [loc for loc in locations]
    # Finding lone locations
    if len(locationList) > 1:

        findLoners = DBSCAN(eps=settings['clusterDistance'], min_samples=1)
        findLoners.fit_predict(locsToPos(locationList), sample_weight=[int('QuestHub' in location or 'WorldZone' in location) for location in locationList])

        loners = [locationList[labelId] for labelId, label in enumerate(findLoners.labels_) if label == -1]
        unnamedHubs = {}
        # Clustering them into unnamed hubs
        if len(loners) > 1:
            clusterLoners = AgglomerativeClustering(n_clusters=None, distance_threshold=settings['clusterDistance'])
            clusterLoners.fit_predict(locsToPos(loners))

            for labelId, label in enumerate(clusterLoners.labels_):
                unnamedHubs.setdefault(label, []).append(loners[labelId])
        # Clustering locations around hubs
        centroids = locsToPos([location for location in locationList if 'QuestHub' in location or 'WorldZone' in location]) + [numpy.average(locsToPos(hub), axis=0) for hub in unnamedHubs.values()]

        hubClustering = KDTree(centroids)
        labels = hubClustering.query(locsToPos(locationList), k=1)

        clusters = {}

        for labelId, label in enumerate(labels[1]):
            clusters.setdefault(label[0], []).append(locationList[labelId])
        # Merge clusters with similar names
        clusterByNames = {}

        for clusterId, cluster in enumerate(clusters.values()):

            names = []

            for location in cluster:

                for contentType in [ct for ct in ['QuestHub', 'WorldZone'] if ct in location]:
                    names.extend([LocalizedStrings[hub['localizedTextIdName']] for hub in location[contentType].values()])
            
            if names:
                clusterByNames.setdefault(names[0], []).extend(cluster)

            else:
                clusterByNames.setdefault(f'Unnamed Location {clusterId}', []).extend(cluster)
        # Merge clusters
        mergedLocations = []

        for cluster in clusterByNames:

            posX, posY = numpy.average(locsToPos(clusterByNames[cluster]), axis=0)

            clusterDict = {'position0':str(posX), 'position2':str(posY), 'clusterName':cluster}

            for location in clusterByNames[cluster]:
                for key in [key for key in location if type(location[key]) is dict]:

                    clusterDict.setdefault(key, {}).update(location[key])

            mergedLocations.append(clusterDict)

        return mergedLocations

    else:
        return locationList
