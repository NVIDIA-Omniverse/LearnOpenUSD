# Deinstancing Refinement

![](../../images/asset-modularity-instancing/slides/Slide40.jpg)

## Exercise: Deinstance Refinement

If we wanted to hide the decal on a box, a simple approach is to use de-instancing. We will lose some optimization in the process, but get back full editability for that copy of the box.

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_deinstance_refine\Scenario.usd  --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.

![](../../images/asset-modularity-instancing//top-left-box-closeup.png)

3. **Click** *Window > Interpreter* to open the Interpreter window.
4. **Run** the following code in the Interpreter window:
```python
box = usdviewApi.prim
box.SetInstanceable(False)
decal = box.GetChild("SM_CubeBox_A04_Decal_01")
decal_vis = decal.GetAttribute("visibility")
decal_vis.Set(UsdGeom.Tokens.invisible)
```

This code de-instanced the cube box asset we selected by setting the instanceable metadata to false. We were then able to edit the child decal prim to hide it without any problems. You box should look like this now with the hidden decal:

![](../../images/asset-modularity-instancing//hidden-decal.png)

5. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

The downside is that we are introducing more total prims by using less instancing. Here's a summarized comparison:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
1 De-instanced Box | 1741 | 1449 | 3

Let's say we needed to make changes to more boxes. Let's apply the same decal visibility change to another box.

6. **Click** on the box to the right of your current selection in the Viewport.

![](../../images/asset-modularity-instancing//middle-box.png)

7. **Run** the following code in the Interpreter window:
```python
box = usdviewApi.prim
box.SetInstanceable(False)
decal = box.GetChild("SM_CubeBox_A04_Decal_01")
decal_vis = decal.GetAttribute("visibility")
decal_vis.Set(UsdGeom.Tokens.invisible)
```

The decal on that box should now be hidden too.

![](../../images/asset-modularity-instancing//hidden-decals-2.png)

8. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

The more we de-instance, the more optimizations we lose. Here's a summarized comparison:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
1 De-instanced Box | 1741 | 1449 | 3
2 De-instanced Boxes | 1771 | 1448 | 3

While simple and convenient, this refinement approach is significantly more unoptimized than others if you are making identical refinements to more than one asset. The next refinement examples will show more optimal approaches to achieve the same.

9. **Close** usdview.