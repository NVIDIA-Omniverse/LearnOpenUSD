# Exercise: Groups

In this exercise, we recreated the `city_blockA` assembly asset, but we will show the use of the `group` kind to section our buildings in the model hierarchy into the north and south sides of the street.

1. In Visual Studio Code, **open** the following file: `asset_structure/exercise_11/create_assembly_with_groups.py`

2. **Add** the code below into the designated section:

```py
### Update - Added for loop for street sides
for side in Side:
    ### Update - Added an intermediate group prim between /World and the building references.
    side_xform = UsdGeom.Xform.Define(stage, world_prim.GetPath().AppendChild(side.name))
    Usd.ModelAPI(side_xform).SetKind(Kind.Tokens.group)
    for x in range(1,4):
        ref_path: Sdf.Path = side_xform.GetPath().AppendChild(f"lrg_bldgF_{x:02}")
        ref_target_prim = UsdGeom.Xform.Define(stage, ref_path).GetPrim()
        ref_target_prim.GetReferences().AddReference("./lrg_bldgF/lrg_bldgF.usd")
        position_bldg(ref_target_prim, x, side)

```

Here we create two `group` kind prims, `North` and `South`. We’ve updated the code to reference three buildings under each group. The `position_bldg()` function has also been updated to accommodate for this.

3. **Save** the file and then **execute** the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_11\create_assembly_with_groups.py
```
Linux:
```sh
python ./asset_structure/exercise_11/create_assembly_with_groups.py
```

4. **Run** the following command to open the output city_blockA in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_11\city_blockA.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_11/city_blockA.usd
```

Note that there are no visual changes compared to the “Assemblies” exercise. However, we have made a structural change to the scenegraph, as you can see in the tree view.

![](../../images/asset-structure/image5.png)

5. In usdview, click on the "**North**" or "**South**" prim. We can see in the *Meta Data* tab that the `kind` field is set to `group`.

![](../../images/asset-structure/image36.png)

We have successfully created a valid model hierarchy:

```sh
    World (assembly)  
        North (group)  
            lrg_bldgF_01 (component)  
            lrg_bldgF_02 (component)  
            lrg_bldgF_03 (component)  
        South (group)  
            lrg_bldgF_01 (component)  
            lrg_bldgF_02 (component)  
            lrg_bldgF_03 (component)
```