# Ad-Hoc Composition Arc Addition Refinement

Composition arcs can be added on the local layer stack to introduce ad hoc edits to the scene without disabling instancing.

![](../../images/asset-modularity-instancing/slides/Slide43.jpg)

## Exercise: Ad-Hoc Composition Arc Addition Refinement

In this exercise, we'll simulate a box that was damaged in the warehouse. We'll add a "Damaged" stamp on a couple of boxes box while maintaining instancing enabled for them.

1. **Open** `instancing_exercises/src_assets/Assets/Utilities/MiscDecals/MiscDecals.usd` in VSCode to inspect the USDA.

`/_MixinOverrides/DamagedStamp` is a speculative over (override) that introduces a new decal Mesh and Material for the "Damaged" stamp. This is a bit hard-coded to position the stamp perfectly on the "CubeBox_A04_26cm" asset, but it could be designed to be used more modularly so it could be applied to all sort of assets. We're going to use this layer as a reference to refine our boxes as an additional ad-hoc composition arc.

2. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_add_arc_refine\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

3. **Click** *Window > Interpreter* to open the Interpreter window.
4. **Run** the following code in the Interpreter window:
```python
from pathlib import Path
stage = usdviewApi.stage
box1 = stage.GetPrimAtPath("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_18")
box2 = stage.GetPrimAtPath("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_17")
stage_path = Path(stage.GetRootLayer().identifier)
decals_path = stage_path.parent.parent / "src_assets" / "Assets" / "Utilities" / "MiscDecals" / "MiscDecals.usd"
box1.GetReferences().AddReference(str(decals_path), "/_MixinOverrides/DamagedStamp")
box2.GetReferences().AddReference(str(decals_path), "/_MixinOverrides/DamagedStamp")
```

Notice how the top first and second box on the pallet closest to the camera now show a stamp that says, "Damaged".

![](../../images/asset-modularity-instancing//ad-hoc-damaged.png)

5. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

This prints a breakdown of the prim and instancing stats. Here's a summarized comparison to the basic instancing scenario:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
Ad-hoc Arc Refinement | 1741 | 1450 | 4

Because prototypes are built off of composition arcs, introducing a new composition arc to an instance triggers the creation of a new prototype with the modifications that we defined in the new arc.

6. **Close** usdview.