
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import ContentViewerWindow

def soldier_security(window: "ContentViewerWindow"): #'PathSoldierEventWave' ??? Wave info probably server side
    pass

def scientist_analysis(window: "ContentViewerWindow"): #Biology/Botany/Analysis/Diagnostic/Chemistry/Archeology??
    pass

def explorer_stalking(window: "ContentViewerWindow"): #What is this???
    pass

def soldier_assassinate(window: "ContentViewerWindow"):
    # assassination = loadManager['PathSoldierAssassinate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Assassinate {assassination['count']} $(creature={assassination['creature2Id']})", 'PathObjective'))
    pass

def soldier_demolition(window: "ContentViewerWindow"):
    # demolition = loadManager['PathSoldierActivate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Destroy {demolition['count']} $(creature={demolition['creature2Id']})", 'PathObjective'))
    pass

def soldier_rescue(window: "ContentViewerWindow"):
    # rescue = loadManager['PathSoldierActivate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Rescue {rescue['count']} $(creature={rescue['creature2Id']})", 'PathObjective'))
    pass

def soldier_SWAT(window: "ContentViewerWindow"):
    # swat = loadManager['PathSoldierSWAT'][data['objectId']]
    
    # group = loadManager['TargetGroup'].get(swat['targetGroupId'])
    
    # if group:
    #     groupName = LocalizedStrings[group['DisplayString']]
    
    # if not groupName:

    #     creatures = []

    #     for i in range(7):
    #         creatureId = group[f'data{i}']

    #         if creatureId != '0':
    #             creatures.append(f"$(creature={creatureId})")

    #     groupName = ', '.join(list(set(creatures)))

    # else:
    #     groupName = f'<i>{groupName}</i>'
        
    # self.layout.addWidget(ContentLabel(f"Kill {swat['count']} {groupName} with $(vitem={swat['virtualItemIdDisplay']})", 'PathObjective'))
    pass

def explorer_exploration(window: "ContentViewerWindow"):
    # doorEntrance = loadManager['PathExplorerDoorEntrance'].get(data['objectId'])
    # # There's also Door with group activate and kill
    # if doorEntrance:
    #     self.layout.addWidget(ContentLabel(f"<b>Entrance:</b> $(creature={doorEntrance['creature2IdSurface']})", 'PathObjective'))
    #     self.layout.addWidget(ContentLabel(f"<b>Inside:</b> $(creature={doorEntrance['creature2IdMicro']})", 'PathObjective'))
    #     # 'worldLocation2IdSurfaceRevealed'  Not accurate--probably minimap position
    pass

def explorer_scavenger(window: "ContentViewerWindow"):
    # hunt = loadManager['PathExplorerScavengerHunt'].get(data['objectId'])

    # if hunt:
    #     for i in range(7):
    #         clue = loadManager['PathExplorerScavengerClue'].get(hunt[f'pathExplorerScavengerClueId0{i}'])

    #         if clue:
    #             clueString = LocalizedStrings[clue['Clue']]

    #             creature = loadManager['Creature2'].get(clue['creature2Id'])

    #             if creature:
    #                 clueString += f'\\n$(creature={clue['creature2Id']})'

    #             else:
    #                 test = loadManager['TargetGroup'].get(clue['targetGroupId']) # REWORK ME

    #                 if test:
    #                     clueString += f'\\n{LocalizedStrings[test['DisplayString']]}'

    #             self.layout.addWidget(ContentLabel(clueString, 'QuestObjective'))

    #             pos = loadManager['WorldLocation2'].get(clue['worldLocation2IdMiniMap'])
    #             if pos:
    #                 self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)
    pass

def explorer_vista(window: "ContentViewerWindow"):
    # node = loadManager['PathExplorerNode']

    # for x in node.values():
    #     if x['pathExplorerAreaId'] == data['objectId']:

    #         pos = loadManager['WorldLocation2'].get(x['worldLocation2Id'])
    #         if pos:
    #             self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #         self.addQuestDirections(x['questDirectionId'], 1)
    pass

def explorer_cartography(window: "ContentViewerWindow"): #explore whole map? 'PathExplorerPowerMap'
    pass

def explorer_operation(window: "ContentViewerWindow"):
    # operation = loadManager['PathExplorerActivate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Investigate {operation['count']} $(creature={operation['creature2Id']})", 'PathObjective'))
    pass

def settler_expansion(window: "ContentViewerWindow"):
    # hub = loadManager['PathSettlerHub'][data['objectId']] # Link ressource items?
    pass

def scientist_study(window: "ContentViewerWindow"):
    # study = loadManager['PathScientistFieldStudy'][data['objectId']]

    # for i in range(8):
    #     self.createLabel(study[f'Checklist0{i}'], 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(study[f'worldLocation2IdIndicator0{i}'])
        
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)
    pass

def settler_project(window: "ContentViewerWindow"):
#     # infrastructure =  loadManager['PathSettlerInfrastructure'][data['objectId']] # Link hubs?
#     # self.createLabel(infrastructure.get('Objective'), 'PathObjective')
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

def settler_service(window: "ContentViewerWindow"):
    # mayor = loadManager['PathSettlerMayor'][data['objectId']] # Add locations of objectives to map

    # for i in range(8):
    #     self.createLabel(mayor.get(f'0{i}'), 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(mayor[f'worldLocation2Id0{i}'])
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #     self.addQuestDirections(mayor.get(f'questDirectionId0{i}'), i + 1)
    pass

def settler_safety(window: "ContentViewerWindow"):
    # sheriff = loadManager['PathSettlerSheriff'][data['objectId']]

    # for i in range(8):
    #     descriptionId = LocalizedStrings[sheriff.get(f'Description0{i}')]
    #     if descriptionId:
    #         self.layout.addWidget(ContentLabel(f"{descriptionId}\\n$(quest={sheriff.get(f'quest2IdSheriff0{i}', '0')})", 'PathObjective'))
    pass

def settler_cache(window: "ContentViewerWindow"):
    pass
