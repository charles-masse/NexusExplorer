<h1 align="center">Nexus Explorer</h1>

![Static Badge](https://img.shields.io/badge/Status-Work_in_Progress-orange) [![Run Tests](https://github.com/charles-masse/NexusExplorer/actions/workflows/test.yml/badge.svg)](https://github.com/charles-masse/NexusExplorer/actions/workflows/test.yml) <!-- Pytest Coverage Comment:Begin -->.<!-- Pytest Coverage Comment:End -->

![Demo](/../gh-images/images//demo.gif)

Explore the worlds of the defunct MMORPG **WildStar**.

**NexusExplorer** is a tool that allows you to browse extracted minimap, model and world data including dialog not present on [JabbitHole](https://www.jabbithole.com/).

## Installation
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

- Clone the repo and install dependencies :
```
git clone https://github.com/charles-masse/NexusExplorer.git
cd NexusExplorer
uv sync
```

- You will need the game assets extracted with a tool like [NexusVault](https://github.com/MarbleBag/NexusVault-CLI).
> [!TIP]
> To export everything with NexusVault, point to your game's `Patch/ClientData.archive` with `archive-path PATH_TO_ARCHIVE` and :
> ```
> > search \\
> > export
> ```

- Extract also one language file (e.g.:`en-US.csv` from `Patch/ClientEn.archive`).

## How to use NexusExplorer

- Go to the cloned repo and :
```
uv run nexus_explorer "PATH_TO_EXTRACTED_GAME_DATA"
```

- Use the WorldSelect window to choose the world you want to load.

![WorldSelect](/../gh-images/images//worldSelect.png)
> [!NOTE]
> **[WORLD_ID]** MAP_NAME **(NUMBER_OF_FEATURES)**

- Explore the map features by clicking on the different icons.

![MapViewer](/../gh-images/images//mapViewer.png)
> [!TIP]
> By clicking on the minimap, the in-game teleport command for this location will be copied to your clipboard.

![linked game object](/../gh-images/images//linkedObject.png)
> [!TIP]
> You can click on underlined names to have more info on that game object.

## Roadmap
- [x] Display minimap
- [x] Cluster map features
- [x] Show Quests
- [x] Show Challenges
- [x] Show Events
- [X] Show Datacubes
- [X] Show Quest and Event objectives
- [X] Show Path missions
- [X] Show quest/mission objectives on map
- [ ] Linked items
- [ ] Show Episodes/Quest chains
- [ ] Linked NPC/creature models
- [ ] Show Nemesis (?)
- [ ] Communicator messages (?)
