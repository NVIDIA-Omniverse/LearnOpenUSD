# Exercise: Assemblies

In this exercise, we will create a new {term}`assembly asset <Assembly>` called `city_blockA` that will {term}`reference <Reference>` `lrg_bldgF` multiple times to create a city block. We will set the {term}`model <Model>` {term}`kind <Kind>` of the {term}`new asset <Asset>` to `assembly`.

1. In Visual Studio Code, **open** the following file: `asset_structure/exercise_10/create_assembly.py`

2. First, let’s set the model kind to assembly. **Add** the code below into the designated PART 1 section:

```py
Usd.ModelAPI(world_prim).SetKind(Kind.Tokens.assembly)
```

3. Now we will populate the asset by referencing the {term}`component assets <Component>`.

```py
for x in range(1,7):
    ref_path: Sdf.Path = world_prim.GetPath().AppendChild(f"lrg_bldgF_{x:02}")
    ref_target_prim = UsdGeom.Xform.Define(stage, ref_path).GetPrim()
    ref_target_prim.GetReferences().AddReference("./lrg_bldgF/lrg_bldgF.usd")
    position_bldg(ref_target_prim, x)
```

Assemblies aggregate assets made up of component assets or other assemblies. Here we are referencing `lrg_bldgF` six times and positioning them into a city block.

4. **Save** the file and then **execute** the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_10\create_assembly.py
```
Linux:
```sh
python ./asset_structure/exercise_10/create_assembly.py
```

5. **Run** the following command in Visual Studio Code to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_10\city_blockA.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_10/city_blockA.usd
```

![](../../images/asset-structure/image44.png)

6. In usdview, click on the "**World**" (default) prim in the tree view. Note that the *Meta Data* tab shows that the `kind` field is set to `assembly`. This is an assembly asset.

![](../../images/asset-structure/image3.png)

7. In usdview, click on "**`lrg_bldgF_01`**" prim in the tree view. Note that the *Meta Data* tab shows that the `kind` field is set to `component`. This is a component asset.

![](../../images/asset-structure/image54.png)

8. Note that we have created a valid {term}`model hierarchy <Model Hierarchy>`:

```sh
World (assembly)
    lrg_bldgF_01 (component)
    lrg_bldgF_02 (component)
    lrg_bldgF_03 (component)
    lrg_bldgF_04 (component)
    lrg_bldgF_05 (component)
    lrg_bldgF_06 (component)
```