
def soldier_security(content): #'PathSoldierEventWave' ??? Wave info probably server side
    return []

def scientist_analysis(content): #Biology/Botany/Analysis/Diagnostic/Chemistry/Archeology??
    return []

def explorer_stalking(content): #What is this???
    return []

def soldier_assassinate(content):
    # assassination = loadManager['PathSoldierAssassinate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Assassinate {assassination['count']} $(creature={assassination['creature2Id']})", 'PathObjective'))
    return []

def soldier_demolition(content):
    # demolition = loadManager['PathSoldierActivate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Destroy {demolition['count']} $(creature={demolition['creature2Id']})", 'PathObjective'))
    return []

def soldier_rescue(content):
    # rescue = loadManager['PathSoldierActivate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Rescue {rescue['count']} $(creature={rescue['creature2Id']})", 'PathObjective'))
    return []

def soldier_SWAT(content):
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
    return []

def explorer_exploration(content):
    # doorEntrance = loadManager['PathExplorerDoorEntrance'].get(data['objectId'])
    # # There's also Door with group activate and kill
    # if doorEntrance:
    #     self.layout.addWidget(ContentLabel(f"<b>Entrance:</b> $(creature={doorEntrance['creature2IdSurface']})", 'PathObjective'))
    #     self.layout.addWidget(ContentLabel(f"<b>Inside:</b> $(creature={doorEntrance['creature2IdMicro']})", 'PathObjective'))
    #     # 'worldLocation2IdSurfaceRevealed'  Not accurate--probably minimap position
    return []

def explorer_scavenger(content):
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
    return []

def explorer_vista(content):
    # node = loadManager['PathExplorerNode']

    # for x in node.values():
    #     if x['pathExplorerAreaId'] == data['objectId']:

    #         pos = loadManager['WorldLocation2'].get(x['worldLocation2Id'])
    #         if pos:
    #             self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #         self.addQuestDirections(x['questDirectionId'], 1)
    return []

def explorer_cartography(content): #explore whole map? 'PathExplorerPowerMap'
    return []

def explorer_operation(content):
    # operation = loadManager['PathExplorerActivate'][data['objectId']]
    # self.layout.addWidget(ContentLabel(f"Investigate {operation['count']} $(creature={operation['creature2Id']})", 'PathObjective'))
    return []

def settler_expansion(content):
    # hub = loadManager['PathSettlerHub'][data['objectId']] # Link ressource items?
    return []

def scientist_study(content):
    # study = loadManager['PathScientistFieldStudy'][data['objectId']]

    # for i in range(8):
    #     self.createLabel(study[f'Checklist0{i}'], 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(study[f'worldLocation2IdIndicator0{i}'])
        
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)
    return []

def settler_project(content):
#     # infrastructure =  loadManager['PathSettlerInfrastructure'][data['objectId']] # Link hubs?
#     # self.createLabel(infrastructure.get('Objective'), 'PathObjective')
    return []

def scientist_speciment(content):
    # specimen = loadManager['PathScientistSpecimenSurvey'][data['objectId']]

    # for i in range(10):
    #     self.createLabel(specimen[f'Objective0{i}'], 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(specimen[f'worldLocation2Id0{i}'])
        
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #     self.addQuestDirections(specimen[f'questDirectionId0{i}'], i + 1)
    return []

def scientist_datacube(content):
    return []

def settler_service(content):
    # mayor = loadManager['PathSettlerMayor'][data['objectId']] # Add locations of objectives to map

    # for i in range(8):
    #     self.createLabel(mayor.get(f'0{i}'), 'QuestObjective')

    #     pos = loadManager['WorldLocation2'].get(mayor[f'worldLocation2Id0{i}'])
    #     if pos:
    #         self.mapView.drawObjective(pos['position0'], pos['position2'], i + 1)

    #     self.addQuestDirections(mayor.get(f'questDirectionId0{i}'), i + 1)
    return []

def settler_safety(content):
    # sheriff = loadManager['PathSettlerSheriff'][data['objectId']]

    # for i in range(8):
    #     descriptionId = LocalizedStrings[sheriff.get(f'Description0{i}')]
    #     if descriptionId:
    #         self.layout.addWidget(ContentLabel(f"{descriptionId}\\n$(quest={sheriff.get(f'quest2IdSheriff0{i}', '0')})", 'PathObjective'))
    return []

def settler_cache(content):
    return []
