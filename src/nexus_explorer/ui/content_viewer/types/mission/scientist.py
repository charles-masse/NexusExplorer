
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nexus_explorer.ui.content_viewer import ContentViewerWindow


def scientist_analysis(window: "ContentViewerWindow"):  #Biology/Botany/Analysis/Diagnostic/Chemistry/Archeology??
    pass

def scientist_study(window: "ContentViewerWindow"):

    # study = loadManager['PathScientistFieldStudy'][data['objectId']]

    # for i in range(8):
    #     self.createLabel(study[f'Checklist0{i}'], 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(study[f'worldLocation2IdIndicator0{i}'])
        
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)
    pass

def scientist_experimentation(window: "ContentViewerWindow"):
    pass

def scientist_speciment(window: "ContentViewerWindow"):

    # specimen = loadManager['PathScientistSpecimenSurvey'][data['objectId']]

    # for i in range(10):
    #     self.createLabel(specimen[f'Objective0{i}'], 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(specimen[f'worldLocation2Id0{i}'])
        
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #     self.addQuestDirections(specimen[f'questDirectionId0{i}'], i + 1)
    
    pass

def scientist_datacube(window: "ContentViewerWindow"):
    pass
