
from typing import TYPE_CHECKING
from urllib.parse import quote

from ..utilities import add_mission_locations, get_mission_context

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow

def scientist_analysis(window: "ContentViewerWindow"):
    #TODO buffs
    content, loading_manager = get_mission_context(window)

    icon = loading_manager['PathScientistCreatureInfo'].get(content['objectId'], {}).get('displayIcon') or ''
    window.add_label("Scan.", 'LabelObjective', icon=icon)
    #Target location
    add_mission_locations(window, content, '1')

def scientist_study(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

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
    add_mission_locations(window, content, '-1')

def scientist_experimentation(window: "ContentViewerWindow"):
    #In creature2, 'pathScientistExperimentationId' == content['objectId']
    content, loading_manager = get_mission_context(window)

    experiment_id = 1

    for experiment in loading_manager['PathScientistExperimentationPattern'].values():
        if experiment['pathScientistExperimentationId'] == content['objectId']:
            #Linked mission
            mission = loading_manager['PathMission'].get(experiment['pathMissionId'])
            if mission:
                #Description
                window.add_label(f'<b><a style="color: rgb(125, 251, 182);" href="{quote(str(mission))}">{experiment['localizedTextIdDescription']}</a></b>', 'LabelObjective', icon=experiment['iconAssetPath'])
                #Map icons
                for x in range(4):
                    loc = loading_manager['WorldLocation2'].get(mission[f'worldLocation2Id0{x}'])
                    if loc:
                        window.add_map_location(loc, str(experiment_id))

            experiment_id += 1
    #Start location(s)
    add_mission_locations(window, content, '-1')

def scientist_speciment(window: "ContentViewerWindow"):

    content, loading_manager = get_mission_context(window)

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
    add_mission_locations(window, content, '-1')

def scientist_datacube(window: "ContentViewerWindow"):
    #Find all datacubes #TODO put in the right zone
    pass
