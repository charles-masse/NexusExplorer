# NexusExplorer
Explore the worlds of the defunct MMORPG **Wildstar**.

NexusExplorer is a tool that allows you to browse extracted minimap, model and world data including dialog not present on [JabbitHole](https://www.jabbithole.com) and unfinished content.

## Requirements
`numpy`, `PyQt6`, `Pillow`, `trimesh`, `PyOpenGL`, `pyperclip`, `scikit-learn`
You can install them with:
```bash
pip install -r requirements.txt
```

## Installation
- You will need the game assets extracted with a tool like [NexusVault](https://github.com/MarbleBag/NexusVault-CLI).
> [!TIP]
> To export everything with NexusVault, point to your game's `Patch/ClientData.archive` with the commands :
```bash
>archive-path PATH_TO_ARCHIVE
>search \\
>export
```
- Make sure you export at least one language file (e.g.:`en-US.csv` from `Patch/ClientEn.archive`).
- Edit the `settings.json` with the path to the exported assets and the name of the language file you want to use:
```JSON
{
    "gameFiles" : "Nexusvault/output/export",
    "language" : "en-US"
}
```

## How to use NexusExplorer
- Run `main.py`
- Use the WorldSelect window to choose the world you want to load.
> [!NOTE]
> [WORLD_ID] MAP_NAME (NUMBER_OF_FEATURES)

![WorldSelect](https://github.com/charlesmasse/NexusExplorer/blob/main/images/worldSelect.png)

- Explore the map features by clicking on the different icons.
> [!TIP]
> By clicking somewhere on the map, the in-game teleport command for this location will be copied to your clipboard.

![MapViewer](https://github.com/charlesmasse/NexusExplorer/blob/main/images/mapViewer.png)