# Exercise: Lofting Primvars

The `accentColor` {term}`primvar <Primvar>` that we added in the “Asset Parameterization” exercise is now hidden behind the {term}`payload <Payload>`. When the payload is {term}`unloaded <Load and Unload>`, consumers can't easily discover this {term}`asset <Asset>` parameter. In this exercise, we will loft the `accentColor` primvar above the payload so that it is still discoverable even with the payload unloaded.

1. In Visual Studio Code, **open** the following file:   
   `asset_structure/exercise_07/lrg_bldgF.usd`.

Note that the `accentColor` primvar is not present in this file.

```usda
#usda 1.0
(
	defaultPrim = "World"
	metersPerUnit = 0.01
	upAxis = "Y"
)

def Xform "World" (
	prepend payload = @./contents.usd@
)
{
}
```

2. In Visual Studio Code, **open** the following file: `asset_structure/exercise_07/loft_parameters.py`

3. Let’s add the code to loft our properties. **Add** the code below into the block:

```py
prim_spec = contents_layer.GetPrimAtPath("/World")
prop_spec: Sdf.PropertySpec
for prop_spec in prim_spec.properties:
    Sdf.CopySpec(contents_layer, prop_spec.path, asset_layer, prop_spec.path)
    prim_spec.RemoveProperty(prop_spec)
```

This code uses the Sdf API, which is a bit lower-level than the Usd API and operates on individual {term}`layers <Layer>` without considering {term}`composition <Composition>`. Here, we're copying all the {term}`properties <Property>` found on the default {term}`prim <Prim>` in `contents.usd` and moving them to the same prim in `lrg_bldgF.usd`. Specifically, we're interested in the `primvars:accentColor` {term}`attribute <Attribute>` so that it's discoverable even when the payload is unloaded.

4.  **Save** the file and then **execute** the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_07\loft_parameters.py
```
Linux:
```sh
python ./asset_structure/exercise_07/loft_parameters.py
```

5. **Open** the output `lrg_bldgF` in usdview by running the following command in Visual Studio Code:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_07\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_07/lrg_bldgF.usd
```

6. In usdview, click on the "**World**” (default) prim. Note the “`primvars:accentColor`” attribute in the *Properties* panel.

![](../../images/asset-structure/image59.png)

7. In usdview, right-click on the “**World**” (default) prim and select “**Unload**”. Note that the “`primvars:accentColor`” attribute is still listed in the *Properties* panel.

![](../../images/asset-structure/image13.png)