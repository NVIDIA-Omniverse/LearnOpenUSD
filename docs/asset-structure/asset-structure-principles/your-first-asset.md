# Exercise: Your First Asset

Let’s take a look at `export.usd` in usdview.

1. In the Visual Studio Code terminal, **run** the following command:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_01\export.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_01/export.usd
```

Take a second to look at the tree view in the top left corner.

![](../../images/asset-structure/image1.png)

Notice that the mesh and material {term}`prims <Prim>` don't have a common ancestor prim that could be referenced to include them all together. Even though the “root” item in the tree view looks like an ancestor prim, it represents the {term}`stage <Stage>`’s {term}`pseudo-root <Pseudo-Root>` and is not a defined prim. We can address this by creating an entry point prim and making all the current root prims its children.

2.  In Visual Studio Code, **open** the following file: `asset_structure/exercise_01/make_entry_point.py`

3. In our script, we will define a `World` prim under which the rest of the prims will be reparented. **Add** the code below into the block:

```py
# Move all root prims under new entry point prim.
editor = Usd.NamespaceEditor(stage)
for prim in root_prims:
    editor.ReparentPrim(prim, world_prim)
    # NamespaceEditor takes care of updating all relationship targets (e.g. material bindings)
    editor.ApplyEdits()
```

4. **Save** the file and then **run** the script using the following command:  
   
Windows:
```powershell
python .\asset_structure\exercise_01\make_entry_point.py
```
Linux:
```sh
python ./asset_structure/exercise_01/make_entry_point.py
```

5.  The output will now be in `lrg_bldgF.usd`. **Run** the following command so we can view this in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_01\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_01/lrg_bldgF.usd
```

6. If the “root” dropdown is not expanded when the file opens, **expand** it now. Notice how all of our prims are now under `World`.

![](../../images/asset-structure/image10.png)

7. Now that we have a fully referenceable {term}`asset <Asset>`, we’ll create a new {term}`layer <Layer>` called `scene.usda` that contains three {term}`references <Reference>` of `lrg_bldgF.usd`. In Visual Studio Code, **run** the following command in the terminal:

Windows:
```powershell
python .\asset_structure\exercise_01\reference_asset.py
```
Linux:
```sh
python ./asset_structure/exercise_01/reference_asset.py
```

8. Next, take a look at our new file in usdview. **Run** the following command so we can open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_01\scene.usda
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_01/scene.usda
```

![](../../images/asset-structure/image27.png)

Notice that when referencing the building, all associated materials and geometry are also included. If we hadn't consolidated these into a single entry point, there would be no clear indication of what should be brought over.