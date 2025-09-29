# Exercise: Reference/Payload Pattern

In this exercise, we will add a reference/payload pattern to our asset. First, we'll export the asset root layer (`lrg_bldF.usd`) and rename it to `contents.usd` to serve as our payload. Next, we'll recreate the asset root layer, omitting the sublayers that have been moved behind the payload. This new root layer will also include the payload arc.

1.  In Visual Studio Code, **open** the following file: `asset_structure/exercise_06/create_payload.py`

2. Let’s add code to create the payload. **Add** the following code into the designated PART 1 section:

```py
stage: Usd.Stage = Usd.Stage.Open(str(working_dir / "lrg_bldgF.usd"))
# "Save As..." the lrg_bldgF.usd as contents.usd
asset_layer: Sdf.Layer = stage.GetRootLayer()
contents_layer_name = "contents.usd"
asset_layer.Export(str(working_dir / contents_layer_name), args={"format": "usda"})
```

This is essentially performing a “Save As…” to save the asset root layer as `content.usd`. This will be the layer that we will payload.

3. Let’s make our asset root layer payload the `contents.usd` layer. **Add** the following code into the designated PART 2 section:

```py
# Create a new asset_layer in memory for now.
stage: Usd.Stage = Usd.Stage.CreateInMemory()
world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
stage.SetDefaultPrim(world_prim)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Add contents.usd as a payload
world_prim.GetPayloads().AddPayload(f"./{contents_layer_name}")
stage.GetRootLayer().Export(str(working_dir / "lrg_bldgF.usd"), args={"format": "usda"})
```

This is creating the asset root layer from scratch, but this time we won’t add any workstream sublayers since those are handled by contents.usd now. Before saving the stage, we add the payload to the `defaultPrim`.

4. **Save** the file and then **execute** the script with the following command:

Windows:
```powershell
python .\asset_structure\exercise_06\create_payload.py
```
Linux:
```sh
python ./asset_structure/exercise_06/create_payload.py
```

You will see a warning message in the console. 
```
Warning: in _ReportErrors at line 3309 of C:\a\OpenUSD\OpenUSD\pxr\usd\usd\stage.cpp -- In </World>: Could not open asset @contents.usd@ for payload introduced by @anon:000001D317F052B0:tmp.usda@</World>. (recomposing stage on stage @anon:000001D317F052B0:tmp.usda@ <000001D31794A9E0>)
```

This is expected because we set a relative path for the payloaded layer, which is invalid while the stage only exists in memory. Once we save the stage to disk and reopen it, everything will compose correctly.

5. In Visual Studio Code, **open** the following file: `asset_structure/exercise_06/lrg_bldgF.usd`. Note the payload arc in this layer now.

6. Let’s see `lrg_bldgF` in a stage where it is referenced. **Open** `lrg_bldgF` in usdview by **running** the following command the Visual Studio Code terminal. 

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_06\scene.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_06/scene.usd
```

The “**building**” Xform is the root of our `lrg_bldgF` asset.  
![](../../images/asset-structure/image67.png)

7. In usdview, right-click on the “**building**” prim and select “**Unload**”. As expected, the descendant prims of “**building**” have disappeared from the tree view and the building no longer appears in the viewport.

![](../../images/asset-structure/image46.gif)

8. In usdview, right-click on the “**building**” prim and select “**Load**”. Note that everything loads again.

![](../../images/asset-structure/image55.gif)