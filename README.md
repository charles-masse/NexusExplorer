<h1>Nexus Explorer</h1>

[![Run Tests](https://github.com/charles-masse/NexusExplorer/actions/workflows/test.yml/badge.svg)](https://github.com/charles-masse/NexusExplorer/actions/workflows/test.yml) <!-- Pytest Coverage Comment:Begin --> <a href="https://github.com/charles-masse/NexusExplorer/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-87%25-green.svg" /></a> <!-- Pytest Coverage Comment:End --> [![XERJ Corpus Hub contributor](https://hub.xerj.org/contributors/charles-masse/badge.svg)](https://hub.xerj.org/contributors/charles-masse)

![Demo](/../gh-images//demo.gif)

Explore the worlds of the defunct MMORPG **WildStar**.

**NexusExplorer** is a tool that allows you to browse extracted minimap, model and world data including dialog not present on [JabbitHole](https://www.jabbithole.com/).

## Installation

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

### Installation from release [Option 1]

- Check the latest release on [GitHub](https://github.com/charles-masse/NexusExplorer/releases).

```bash
uv tool install https://github.com/charles-masse/NexusExplorer/releases/download/v0.8.0/nexusexplorer-0.8.0-py3-none-any.whl
```

### Installation from source [Option 2]

- Clone the repo and install the tool :

```bash
git clone https://github.com/charles-masse/NexusExplorer.git
cd NexusExplorer
uv tool install .
```

### Extracting the game data [Required]

- You will need the game assets extracted with a tool like [NexusVault](https://github.com/MarbleBag/NexusVault-CLI).

> [!TIP]
> To export everything with NexusVault, point to your game's `Patch/ClientData.archive` with `archive-path PATH_TO_ARCHIVE` and :
>
> ```bash
> search \\
> export
> ```

- Extract also one language file (e.g.:`en-US.csv` from `Patch/ClientEn.archive`).

## How to use NexusExplorer

```bash
nexus_explorer "PATH_TO_EXTRACTED_GAME_DATA"
```

- Use the WorldSelect window to choose the world you want to load.

![WorldSelect](/../gh-images//worldSelect.png)
> [!NOTE]
> **[WORLD_ID]** MAP_NAME **(NUMBER_OF_FEATURES)**

- Explore the map features by clicking on the different icons.

![MapViewer](/../gh-images//mapViewer.png)
> [!TIP]
> By clicking on the minimap, the in-game teleport command for this location will be copied to your clipboard.

![linked game object](/../gh-images//linkedObject.png)
> [!TIP]
> You can click on underlined names to have more info on that game object.

## Special Mention

[Wildstar Lore Export](https://wildstar-lore-export.vercel.app/) - A great tool to explore the lore of WildStar without needing to extract the game files.
