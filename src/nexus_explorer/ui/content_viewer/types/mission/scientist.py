
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def scientist_analysis(window: "ContentViewerWindow"):
    #TODO buffs
    content = window.content
    loading_manager = window.loading_manager

    icon = loading_manager['PathScientistCreatureInfo'].get(content['objectId'], {}).get('displayIcon') or ''
    window.add_label("Scan.", 'LabelObjective', icon)
    #Target location
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '1')

def scientist_study(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager

    study = loading_manager['PathScientistFieldStudy'][content['objectId']]
    if study:
        #Objectives
        for i in range(8):
            window.add_label(study[f'localizedTextIdChecklist0{i}'], 'LabelObjective')
            #Map icon
            loc = loading_manager['WorldLocation2'].get(study[f'worldLocation2IdIndicator0{i}'])
            if loc:
                window.add_map_location(loc, str(i + 1))
    #Start location(s)
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '-1')

def scientist_experimentation(window: "ContentViewerWindow"):
    #TODO link to the other path mission
    content = window.content
    loading_manager = window.loading_manager

    experiment = loading_manager['PathScientistExperimentationPattern']
    for i, x in enumerate(experiment.values()):
        if x['pathScientistExperimentationId'] == content['objectId']:
            #Description
            window.add_label(x['localizedTextIdDescription'], 'LabelObjective', "C:/Users/charl/Documents/scripts/NexusExplorer/Nexusvault/output/export/UI/Icon/Item/Misc/rune_0001/rune_0001.png")
            #Linked mission
            mission = loading_manager['PathMission'].get(x['pathMissionId'])
            if mission:
                for i in range(4):
                    loc = loading_manager['WorldLocation2'].get(mission[f'worldLocation2Id0{i}'])
                    if loc:
                        window.add_map_location(loc, str(i + 1))

            break
    #Start location(s)
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '-1')

def scientist_speciment(window: "ContentViewerWindow"):

    content = window.content
    loading_manager = window.loading_manager

    specimen = loading_manager['PathScientistSpecimenSurvey'].get(content['objectId'])

    if specimen:
        for i in range(10):
            #Text
            window.add_label(specimen[f'localizedTextIdObjective0{i}'], 'LabelObjective')
            #Objectives
            loc = loading_manager['WorldLocation2'].get(specimen[f'worldLocation2Id0{i}'])
            if loc:
                window.add_map_location(loc, str(i + 1))
            #Quest directions
            directions = loading_manager['QuestDirection'].get(specimen[f'questDirectionId0{i}'])
            if directions:
                for x in range(16):
                    entry_id = directions.get(f'questDirectionEntryId{str(x).zfill(2)}')
                    dir = loading_manager['QuestDirectionEntry'].get(entry_id)
                    if dir:
                        loc = loading_manager['WorldLocation2'].get(dir['worldLocation2Id'])
                        if loc:
                            window.add_map_location(loc, str(i + 1))
    #Start location(s)
    for i in range(4):
        loc = loading_manager['WorldLocation2'].get(content[f'worldLocation2Id0{i}'])
        if loc:
            window.add_map_location(loc, '-1')

def scientist_datacube(window: "ContentViewerWindow"):
    #Find all datacubes #TODO put in the right zone
    pass
