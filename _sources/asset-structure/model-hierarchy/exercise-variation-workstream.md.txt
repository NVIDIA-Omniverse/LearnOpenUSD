# Exercise: Variation Workstream

In this exercise, we'll simulate a surfacing artist working at the assembly level to make shading variation choices on multiple buildings in `city_blockA`. We've added a shading workstream to `city_blockA`, allowing a surfacing artist to work at the city block context and see how their variation choices on individual buildings look in context.

To simulate a surfacing artist working on `city_blockA`, you'll create a script that makes random `accentColor` and `exteriorType` choices. These choices will be authored to the `contents/shading.usd` sublayer of the `city_blockA` asset.

1. **Run** the following command in Visual Studio Code to open `city_blockA` in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_12\city_blockA.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_12/city_blockA.usd
```

![](../../images/asset-structure/image33.png)

Note the starting state of `city_blockA`. All of the buildings have a stucco exterior and red awning.

2. In Visual Studio Code, **open** the following file: `asset_structure/exercise_12/set_bldg_variations.py`
3. Let’s complete our script for randomizing the building variations. **Add** the code below into the block:

```py
for prim in stage.Traverse():
    if prim.IsComponent() and prim.GetVariantSets().HasVariantSet("exteriorType"):
        accent_primvar = UsdGeom.PrimvarsAPI(prim).GetPrimvar("accentColor")
        accent_primvar.Set(random.choice(accent_choices))
        vset = prim.GetVariantSet("exteriorType")
        vset.SetVariantSelection(random.choice(vset.GetVariantNames()))
```

In this snippet, we are traversing through the stage and setting a random variant choice and accent color for every component asset that has an `exteriorType` variant set.

4. **Save** the file and then **execute** the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_12\set_bldg_variations.py
```
Linux:
```sh
python ./asset_structure/exercise_12/set_bldg_variations.py
```

5. The output will now be in `contents/shading.usd`. Let’s go ahead and view the updated asset in `usdview` by **running** the following command in Visual Studio Code:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_12\city_blockA.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_12/city_blockA.usd
```

Your results may look different, but you should now see some variant in the building exterior and accent colors:

![](../../images/asset-structure/image6.png)

You can rerun the script and view the results again in `usdview` if you want to try to get a different randomized result.

6. In Visual Studio Code, **open** the following file:   
   `asset_structure/exercise_12/contents/shading.usd` 

Note the sparse overrides that our script authored in this layer.

![](../../images/asset-structure/image34.png)