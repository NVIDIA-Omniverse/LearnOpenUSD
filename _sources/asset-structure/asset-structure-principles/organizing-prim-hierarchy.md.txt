# Exercise: Organizing Prim Hierarchy

In this exercise, we're going to organize all mesh prims under a new `Geometry` scope and all material prims under a `Looks` scope. This will provide organization and define jurisdictions for products contributed by modelers versus those contributed by surfacers.

1. Let’s take a look back at our building. **Open** the `lrg_bldgF.usd` in usdview by **running** the following command in the Visual Studio Code terminal:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_03\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_03/lrg_bldgF.usd
```

2. **Expand** the root and World dropdowns.

![](../../images/asset-structure/image50.png)

Right now all of our prims are encapsulated in World. It is not immediately clear to downstream users how each prim relates to one another. Let’s separate the materials from the geometry to provide more clarity. 

3. **Open** the following script in Visual Studio Code: `asset_structure/exercise_03/organize_prims.py` 

We see some familiar code reparenting our prims, but this time we are reparenting them based on if they are a mesh or a material. The snippet below shows how we are sorting the prims:

```py
for prim in default_prim_children:
    if prim.IsA(UsdGeom.Mesh):
        editor.ReparentPrim(prim, geom_scope)
        editor.ApplyEdits()
    elif prim.IsA(UsdShade.Material):
        editor.ReparentPrim(prim, looks_scope)
        editor.ApplyEdits()
```

4. Let’s run the script and see how it changes our layer. In the terminal, **run** the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_03\organize_prims.py
```
Linux:
```sh
python ./asset_structure/exercise_03/organize_prims.py
```

5. Now, **open** the file in usdview by **running** the following command:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_03\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_03/lrg_bldgF.usd
```

6. **Expand** the root and World dropdowns if they’re not already expanded.

![](../../images/asset-structure/image23.png)

Now we can see that our meshes are grouped under our `Geometry` scope and our materials are grouped under `Looks`. This should make it easier for users to find what they’re looking for in the scene.