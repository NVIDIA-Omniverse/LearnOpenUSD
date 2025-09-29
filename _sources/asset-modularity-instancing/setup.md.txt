# Module Setup: Asset Modularity and Instancing 

## Setup Required Tools

This module uses usdview and Python. If you haven't done so yet, please follow the [Installing usdview and Setting Up Python](../usdview-install-instructions.md) instructions before proceeding.

## Get the Exercise Content

This module includes interactive exercises to give you hands-on experience. This section will walk you through how to download and install the exercise content.

1. **Download** the required [*Asset Modularity and Instancing* exercise content](../_static/instancing-exercise-files.zip){.external .download}.
2. **Extract** the folder.
3. **Open** the root folder for the OpenUSD binaries in Visual Studio Code. We named this folder `usd_root/` when installing usdview. If you have not installed usdview refer to [full installation instructions](../usdview-install-instructions.md).
4. **Copy** the extracted folder into `usd_root/` by dragging and dropping it into the *Explorer* section of Visual Studio Code. If prompted about adding the folder to the workspace, select **Copy Folder**.

The folder we want to copy over is the `instancing/` folder.

![](../images/asset-modularity-instancing/copy-instancing-exercises.mp4)

## Activate Your Python Environment

If you have set up a virtual Python environment using our [virtual environment instructions](#setting-up-python-env), then **run** the appropriate command for your operating system in the terminal within Visual Studio Code to start your virtual Python environment.

```{include} ../_includes/venv-table.md
```

You'll need to adapt the commands above if you named your virtual environment differently.

```{attention}
All exercises will assume Visual Studio Code is open in the `usd_root/`. See video above for reference.
```
## usdview Setup

These instructions will guide you in setting up some default settings in usdview to avoid inconsistencies and confusion during the usdview exercises.

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_assets_overview\AssetsLineup.usd
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_assets_overview/AssetsLineup.usd
```

2. In the Viewport panel, **toggle on** only *Lights > Enable Default Dome Light*.

The lighting options in the *Lights* menu to look like this:
![](../images/asset-modularity-instancing/lighting_options.png)

3. In the Viewport panel, **click** *Select > Models*.
![](../images/asset-modularity-instancing/select_models_option.png)

4. In the Tree View panel, **toggle on** all of the options in the *Show* menu. 

The following options should be turned on: *Show > Inactive Prims*, *Show > Prototype Prims*, *Show > Undefined Prims (Overs)*, *Show > Abstract Prims (Classes)*, and *Show > Use Display Names (Prims)*. The *Show* menu should look like this:
![](../images/asset-modularity-instancing/show_options.png)

5. **Close** usdview.