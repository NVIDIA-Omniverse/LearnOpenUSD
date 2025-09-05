# Refinement Using Variant Sets

## What Is Refinement Using Variant Sets?

Your use case may have a common workflow pattern that could be captured as variants or states within your assets.

Variant sets are part of composition and your variant selections are evaluated when OpenUSD determines what implicit prototypes it needs to create. This means that you can edit the subgraphs of your instances through variant selections and OpenUSD will figure out any additional prototypes it needs based on the variants.

A useful pattern is to place your variant sets on the instanceable prim so that you can still make different variant selection even when an asset is instanced. This pattern pairs very well with the asset structure concept of [asset parameterization](../../asset-structure/asset-parameterization/what-is-asset-parameterization.md).

![](../../images/asset-modularity-instancing/variant-set-refinement.png)

In your factory, every box going down the line transitions from an open state to a closed state. Let's say at a given point in your simulation, 50% of your boxes to be open and 50% of your boxes will be closed. You could represent this with a variant set. In this case, all of your boxes can continue to leverage instancing, but you end up with two prototypes instead of one.

## Exercise: Refinement Using Variant Sets

We will use variant sets to add a shipping label decal to a box. This is a standard part of our shipping and receiving workflow so our asset already has a variant set to handle that.

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_varset_refine\Scenario.usd  --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.

![](../../images/asset-modularity-instancing/top-left-box-closeup.png)

3. On the Metadata tab, **set** the "statusVariant" to "allocated".

![](../../images/asset-modularity-instancing//allocated-variant.png)

This adds a shipping label to the top of the box and sets the custom "status" attribute on that prim to "ALLOCATED". We can use these variants to track the status of packages within our facility.

4. **Click** on the box to the right of your current selection in the Viewport.

![](../../images/asset-modularity-instancing/middle-box-label.png)

5. On the Metadata tab, **set** the "statusVariant" to "allocated".

![](../../images/asset-modularity-instancing/allocated-variant-2.png)

6. **Click** *Window > Interpreter* to open the Interpreter window.
7. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

This prints a breakdown of the prim and instancing stats. Here's a summarized comparison to other scenarios:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
1 De-instanced Box | 1741 | 1449 | 3
2 De-instanced Boxes | 1771 | 1448 | 3
2 Allocated Variant Boxes | 1737 | 1450 | 4

Before we were only using one box variant so we had one box prototype. Using a second box variant now, "allocated," introduces a new prototype based on the box asset. Note how this uses less prims than the de-instancing approach. It also scales well. We can switch more boxes to use the "allocated" variant without incrementing the total prim count.

You can see how with a little foresight and planning you can keep the instance refinement experience as simple as de-instancing, but without losing as much optimization.

8. **Close** usdview.