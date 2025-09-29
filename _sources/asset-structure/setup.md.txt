# Module Setup: Asset Structure Principles and Content Aggregation

## Setup Required Tools

This module uses usdview and Python. If you haven't done so yet, please follow the [Installing usdview and Setting Up Python](../usdview-install-instructions.md) instructions before proceeding.

## Get the Exercise Content

This module includes interactive exercises to give you hands-on experience. This section will walk you through how to download and install the exercise content.

1. **Download** the required [*Asset Structure Principles and Content Aggregation* exercise content](../_static/asset-structure-exercise-files.zip){.external .download}.
2. **Extract** the folder.
3. **Open** the root folder for the OpenUSD binaries in Visual Studio Code. We named this folder `usd_root/` when installing usdview. If you have not installed usdview refer to [full installation instructions](../usdview-install-instructions.md).
4. **Copy** the extracted folder into `usd_root/` by dragging and dropping it into the *Explorer* section of Visual Studio Code. If prompted about adding the folder to the workspace, select **Copy Folder**.

The folder we want to copy over is the `asset_structure` folder.
![](../images/asset-structure/asset-structure-copy-activities.webm)

5. If you have set up a virtual Python environment using our [virtual environment instructions](#setting-up-python-env), then **run** the appropriate command for your operating system in the terminal within Visual Studio Code to start your virtual Python environment.

```{include} ../_includes/venv-table.md
```

You'll need to adapt the commands above if you named your virtual environment differently.

```{attention}
All exercises will assume Visual Studio Code is open in the `usd_root/`. See video above for reference.
```