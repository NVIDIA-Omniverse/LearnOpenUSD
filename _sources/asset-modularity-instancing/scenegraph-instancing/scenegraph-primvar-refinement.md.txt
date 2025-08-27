# Refinement through Primvars

![](../../images/asset-modularity-instancing/slides/Slide42.jpg)

## Exercise: Primvar Refinement

In this exercise, we're going to use a custom "cleanness" primvar that we authored for our box asset to control the brightness of the box's cardboard material. In simulation, we could use this as a visual representation of how long a box has been in the warehouse. An older box would appear dirtier or darker than the rest. This would enable us to quickly scan our digital twin and find boxes that have been sitting around for a long time.

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_primvar_refine\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.

![](../../images/asset-modularity-instancing//top-left-box-closeup.png)

3. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected prim in the Tree View.

You should see "CubeBox_A04_26cm_18" selected in the Tree View panel.

4. **Click** the triangle to the left of the select prim in the Tree View to expand the select prim's hierarchy.
5. **Click** the triangle to the left of the "Looks" prim in the Tree View to expand the select prim's hierarchy.
6. **Click** the triangle to the left of the "M_CubeBox_Cardboard_01" prim in the Tree View to expand the select prim's hierarchy.
7. **Click** on "UsdPrimvarReader_cleanness" to select it.

![](../../images/asset-modularity-instancing//primvar-reader.png)

This shader is used by all boxes to check for "primvars:cleanness" on any gprim (e.g. Mesh or Subset) that it's assigned to.

8. **Click** on "UsdPreviewSurface" to select it.
9. **Click** on the triangle to the left of the "inputs:occlusion" attribute in the Property panel expand it.

![](../../images/asset-modularity-instancing//occlusion.png)

This reveals that the output from "UsdPrimvarReader_cleanness" is connected to "inputs:occlusion" to drive the occlusion of this cardboard material. The closer the number gets to "0.0", the darker the material gets.

10. **Click** *Window > Interpreter* to open the Interpreter window.
11. **Run** the following code in the Interpreter window:
```python
stage = usdviewApi.stage
box1 = stage.GetPrimAtPath("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_18")
box2 = stage.GetPrimAtPath("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_17")
box1.GetAttribute("primvars:cleanness").Set([0.8])
box2.GetAttribute("primvars:cleanness").Set([0.6])
```

Note how the two boxes closes to the camera are now darker from the rest.
![](../../images/asset-modularity-instancing//cleanness-set.png)

12. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

This prints a breakdown of the prim and instancing stats. Here's a summarized comparison to the basic instancing scenario:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
Primvar Refinement | 1711 | 1450 | 3

Primvar refinement does not add any prims to the total prim count. All we are doing is authoring a new opinion on the instance prims that are already a part of the total prim count. No new prototypes are created either. The single prototype handles all of the shading variability on its own.

13. **Close** usdview.