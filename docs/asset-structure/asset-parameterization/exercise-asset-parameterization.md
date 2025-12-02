# Exercise: Asset Parameterization

In this exercise, you’ll create a {term}`primvar <Primvar>` as an {term}`asset <Asset>` parameter to control the accent color of the building's awning. Note that we have updated the `lrg_bldgF` asset so that the `roof` material now accepts a primvar for its `diffuseColor`.

1. In Visual Studio Code, **open** the following file: `asset_structure/exercise_05/contents/shading.usd`  
2. Then, **find** the following snippet in the file (it should be around line 86).

```{code-block} usda
:lineno-start: 86

def Shader "PrimvarAccentColor"
{
    uniform token info:id = "UsdPrimvarReader_float3"
    float3 inputs:fallback = (0.3372549, 0.7372549, 0.6)
    string inputs:varname = "accentColor"
    float3 outputs:result
}
```

This material graph now uses a `UsdPrimvarReader_float3` to read a primvar called `primvars:accentColor` with a fallback color if it does not find a primvar. The `inputs:fallback` is the green color we saw previously for the roof.

Let’s explore what happens when we author `primvars:accentColor`. 

3. In Visual Studio Code, **open** the following file: `asset_structure/exercise_05/create_asset_parameters.py`

```py
stage: Usd.Stage = Usd.Stage.Open(str(working_dir / "lrg_bldgF.usd"))
default_prim: Usd.Prim = stage.GetDefaultPrim()
primvars_api = UsdGeom.PrimvarsAPI(default_prim)
accent_color = primvars_api.CreatePrimvar("accentColor", Sdf.ValueTypeNames.Float3, UsdGeom.Tokens.constant)
accent_color.Set((1.0, 0.0, 0.0))
```

In the code, we are creating the primvar using the PrimvarsAPI and setting the color to red.

4. In the terminal, **run** the following command to execute the script:

Windows:
```powershell
python .\asset_structure\exercise_05\create_asset_parameters.py
```
Linux:
```sh
python ./asset_structure/exercise_05/create_asset_parameters.py
```

5. **Run** the following command in the terminal to view the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_05\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_05/lrg_bldgF.usd
```

![](../../images/asset-structure/image43.png)  

At first glance, we can see that the roof is now red. When selecting the **roof** prim in the tree view, then selecting the **`accentColor`** in the *Property* panel, we can observe in the *Meta Data* panel that this accent color is being inherited down the prim hierarchy from the asset parameter we created, rather than from the `UsdPrimvarReader`'s fallback value. The `(i)` symbol next to the attribute name indicates that it is an "inherited property."