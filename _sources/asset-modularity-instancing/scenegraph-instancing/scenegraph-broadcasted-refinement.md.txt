# Broadcasted Refinement

We haven’t reviewed inherits and specializes, but if you’re familiar with those arcs, you’ll know that they compose across arcs to allow downstream refinement.  We call this broadcasting.
So we can used inherits and specializes to refine instances of a Robot within a work cell


![](../../images/asset-modularity-instancing/slides/Slide44.jpg)

## Exercise: Broadcasted Refinement

In this scenario, all the boxes on a pallet were damaged. We want to label all the boxes with the "Damaged" stamp. We could add a new arc to all the affected boxes one by one, but for this example, we're going to use a specialize arc to broadcast the change to all of the boxes on the pallet.


1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_broadcasted_refine\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.

![](../../images/asset-modularity-instancing//top-left-box-closeup.png)

3. **Press** the "<span>&#92;</span>" key to select the enclosing model.

This will select the "BoxPallet_A01" assembly.

![](../../images/asset-modularity-instancing//select-pallet-assembly.png)

4. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected prim in the Tree View.

You should see "BoxPallet_A01_03" selected in the Tree View panel.

5. **Click** the triangle to the left of the select prim in the Tree View to expand the select prim's hierarchy.

![](../../images/asset-modularity-instancing//reveal-specialize-target.png)

Notice that there is a prim "_PalletBox" enclosed within the "BoxPallet_A01" asset. This is a class prim included as specialize arc target for every box on that pallet. We can author opinions in "_PalletBox" that will be applied to all boxes on that pallet.

6. **Click** *Window > Interpreter* to open the Interpreter window.
7. **Run** the following code in the Interpreter window:
```python
from pathlib import Path
stage = usdviewApi.stage
prim = stage.OverridePrim("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/_PalletBox")
stage_path = Path(stage.GetRootLayer().identifier)
decals_path = stage_path.parent.parent / "src_assets" / "Assets" / "Utilities" / "MiscDecals" / "MiscDecals.usd"
prim.GetReferences().AddReference(str(decals_path), "/_MixinOverrides/DamagedStamp")
```

![](../../images/asset-modularity-instancing/damaged-pallet.png)

Notice how all the boxes on the pallet closest to the camera now show a stamp that says, "Damaged". In this case, we added the same reference as in the [Ad-Hoc Composition Arc Addition Refinement](./scenegraph-add-arc-refinement.md) exercise, but this could also have been direct opinions authored in the `/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/_PalletBox` of this layer. We authored one opinion that rippled changes to all the boxes.

8. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

This prints a breakdown of the prim and instancing stats. Here's a summarized comparison to the basic instancing scenario:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
Broadcasted Refinement | 1747 | 1450 | 4

9. **Close** usdview.