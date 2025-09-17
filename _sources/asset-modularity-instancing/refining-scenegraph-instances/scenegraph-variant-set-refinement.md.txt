# Refinement Using Variant Sets

## What Is Refinement Using Variant Sets?

Your use case may have a common workflow pattern that could be captured as variants or states within your assets.

Variant sets are part of composition and your variant selections are evaluated when OpenUSD determines what implicit prototypes it needs to create. This means that you can edit the subgraphs of your instances through variant selections and OpenUSD will figure out any additional prototypes it needs based on the variants.

A useful pattern is to place your variant sets on the instanceable prim so that you can still make different variant selection even when an asset is instanced. This pattern pairs very well with the asset structure concept of [asset parameterization](../../asset-structure/asset-parameterization/what-is-asset-parameterization.md).

![](../../images/asset-modularity-instancing/variant-set-refinement.png)

In your factory, every box going down the line transitions from an open state to a closed state. Let's say at a given point in your simulation, 50% of your boxes to be open and 50% of your boxes will be closed. You could represent this with a variant set. In this case, all of your boxes can continue to leverage instancing, but you end up with two prototypes instead of one.

## Exercise: Refinement Using Variant Sets

### Introduction

In this exercise, you will learn how to use variant sets for refinement, a more efficient approach than [deinstancing](./scenegraph-deinstance-refinement.md) when you need to make the same override on multiple instances. This works well if the override is part of an established workflow since it generally involves encoding the overrides as a part of the source asset.

In our shipping and receive warehouse digital twin, it is typical that we must ship products from our inventory. To visually simulate this in our digital twin, we will add a shipping label to boxes when they are being prepared to ship and when they have been shipped. We have represented these states using a variant set. You'll apply variant selections to add shipping labels to boxes, observe how this creates new prototypes, and compare the performance impact against deinstancing refinement. This technique scales well for common workflow patterns.

### Applying Variant Set Refinement

We will use variant sets to add a shipping label decal to a box. This is a standard part of our shipping and receiving workflow so we created a variant set ahead of time in the CubeBox_A04_26cm asset.

```{seealso}
Explore the asset structure in `instancing/src_assets/Assets/Components/CubeBox_A04_26cm/CubeBox_A04_26cm.usd` to see how we incorporated this variant set. The [Asset Structure Principles and Content Aggregation](../../asset-structure/index.md) module provides another concrete example of authoring variant sets in assets if you want to review this concept further.
```

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_varset_refine\Scenario.usd  --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_varset_refine/Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.

![](../../images/asset-modularity-instancing/top-left-box-closeup.png)

This is the box that we will be shipping.

3. On the Metadata tab, **set** the "statusVariant" to "allocated".

![](../../images/asset-modularity-instancing//allocated-variant.png)

This adds a shipping label to the top of the box and sets the custom `status` attribute on that prim to "ALLOCATED". The custom `status` attribute give us a convenient way to query the box's state instead of just relying on the name of the variant. We can use these variants to track the status of packages within our facility.

### Applying Variants to Multiple Instances

4. **Click** on the box to the right of your current selection in the Viewport.

![](../../images/asset-modularity-instancing/middle-box-label.png)

5. On the Metadata tab, **set** the "statusVariant" to "allocated".

![](../../images/asset-modularity-instancing/allocated-variant-2.png)

### Analyzing the Impact Using Stage Statistics

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

**Key observations:**
- Before we were only using one box variant so we had one box prototype
- Using a second box variant now, "allocated," introduces a new prototype based on the box asset
- Note how this uses fewer prims than the deinstancing approach
- It also scales well - we can switch more boxes to use the "allocated" variant without incrementing the total prim count

You can see how with a little foresight and planning you can keep the instance refinement experience as simple as deinstancing, but without losing as much optimization.

8. **Close** usdview.

### Conclusion

You've successfully learned refinement using variant sets, an efficient technique that creates new prototypes based on variant selections. This approach scales better than deinstancing for common workflow patterns, allowing you to introduce variety while maintaining optimal performance and minimal prim count growth.