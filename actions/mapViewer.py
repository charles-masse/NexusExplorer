
import os

import numpy

from PyQt6.QtCore import QCoreApplication

from sklearn.neighbors import KDTree
from sklearn.cluster import DBSCAN# , AgglomerativeClustering

from PIL import Image, ImageOps

from singletons import settings, LocalizedStrings, loadManager

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

def generateMapImage(worldId, maxCallback, progressCallback):

    mapPath = loadManager['World'][worldId]['assetPath'].replace('\\', '/')
    cachePath = f'./cache/{mapPath}.png'
    chunkPath = f'{settings['gameFiles']}/{mapPath}'

    if os.path.exists(cachePath):
        im = Image.open(cachePath)

    elif not os.path.exists(chunkPath):
        return

    else:
        # Get chunk images
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

    if len(locationList) > 1:
        # Finding lone locations
        findLoners = DBSCAN(eps=settings['clusterDistance'], min_samples=1)

        weight = [
                  1 if any(LocalizedStrings[d.get('localizedTextIdName')] for d in location.get('QuestHub', {}).values())
                  or any(LocalizedStrings[d.get('localizedTextIdName')] for d in location.get('WorldZone', {}).values())
                  else 0
                  for location in locationList
                 ]
        findLoners.fit_predict(locsToPos(locationList), sample_weight=weight)

        loners = [locationList[labelId] for labelId, label in enumerate(findLoners.labels_) if label == -1]
        # Clustering them into unnamed hubs
        unnamedHubs = {}
        
        if len(loners) > 1:
            clusterLoners = DBSCAN(eps=settings['clusterDistance'], min_samples=1)
            clusterLoners.fit_predict(locsToPos(loners))

            for labelId, label in enumerate(clusterLoners.labels_):
                unnamedHubs.setdefault(label, []).append(loners[labelId])
        # Clustering locations around hubs
        namedLocations = [
                          loc for loc in locationList
                          if any(
                                 LocalizedStrings[locData.get('localizedTextIdName')]
                                 for ct in ['QuestHub', 'WorldZone']
                                 for locData in loc.get(ct, {}).values()
                                 if LocalizedStrings[locData.get('localizedTextIdName')]
                                )
                         ]

        centroids = locsToPos(namedLocations) + [numpy.average(locsToPos(hub), axis=0) for hub in unnamedHubs.values()]

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
                # Named Quest Hubs and Zones
                for contentType in [ct for ct in ['QuestHub', 'WorldZone'] if ct in location]:
                    names.extend([LocalizedStrings[hub['localizedTextIdName']] for hub in location[contentType].values()])
                # Named challenge locations
                if 'Challenge' in location:
                    names.extend([LocalizedStrings[challenge.get('localizedTextIdLocation')] for challenge in location['Challenge'].values()])
            
            if names and any(name is not None for name in names):

                selectedName = None

                for name in [n for n in names if n and n != '']:
                    if not selectedName or any(name == clusterName for clusterName in clusterByNames.keys()):
                        selectedName = name

                clusterByNames.setdefault(selectedName, []).extend(cluster)

            else:
                clusterByNames.setdefault(f'Unnamed Location #{clusterId}', []).extend(cluster)
        # Merge clusters
        mergedLocations = []

        for clusterName, clusterData in clusterByNames.items():

            posX, posY = numpy.median(locsToPos(clusterData), axis=0)

            clusterDict = {'clusterName':clusterName, 'position0':str(posX), 'position2':str(posY)}

            for location in clusterData:
                for key in [key for key in location if type(location[key]) is dict]:
                    clusterDict.setdefault(key, {}).update(location[key])

            mergedLocations.append(clusterDict)

        return mergedLocations

    else:
        locationList[0]['clusterName'] = 'Unnamed Location'

        return locationList
