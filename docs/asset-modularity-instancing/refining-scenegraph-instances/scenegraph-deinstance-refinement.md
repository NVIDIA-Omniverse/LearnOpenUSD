# Deinstancing Refinement

## What Is Deinstancing Refinement?

The simplest way to edit or override an instance is to disable instancing for that instance.

```{figure} ../../images/asset-modularity-instancing/deinstance-refinement.mp4
Deinstance refinement
```

At any point downstream, we can enable or disable instancing on a {term}`prim <Prim>`. If we have a use case where we just need to open one box, what we'll do is we'll set `instanceable = false` and now we can apply the overrides to open that box. 

If you just have one thing that needs to be promoted to be treated uniquely from the rest of the copies, it's totally reasonable to deinstance it in a stronger {term}`layer <Layer>`.

You will still benefit from all the performance benefits from {term}`composition <Composition>` and modular {term}`asset <Asset>` reuse. You are just losing a little bit of the instancing performance benefits for the copy you deinstanced.

Deinstancing is simple and convenient, but if you find yourself wanting to deinstance many copies of a prototype to introduce more diversity in your scenes, then one or more of the other refinement techniques may be better suited.

## Exercise: Deinstance Refinement

### Introduction

In this exercise, you will learn the simplest refinement technique: deinstancing. You'll disable instancing on specific instanceable prims to regain full editability, then observe how this affects stage statistics. This approach trades some optimization for complete control over individual instances.

We will pretend we've been asked to hide the decal on box similar to [Exercise: Instance Editability](./scenegraph-instance-refinement.md#exercise-instance-editability), but this time we will apply the override successfully using deinstance refinement.

### Deinstancing a Single Instance

If we wanted to hide the decal on a box, a simple approach is to use deinstancing. We will lose some optimization in the process, but get back full editability for that copy of the box.

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_deinstance_refine\Scenario.usd  --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_deinstance_refine/Scenario.usd --camera ExCam_01
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

```{tip}
usdview has a special `UsdViewApi` object--accessible from `usdviewApi` in the Interpreter window--that gives us convenient context-aware access to our selections. 
```

In Step 2, we selected the instanceable prim we want to deistance. We can get a `Usd.Prim` object for our selection using `usdviewApi.prim`. This code deinstanced the cube box asset by setting `instanceable = false`. We were then able to edit the child decal prim to hide it without any problems. Your box should look like this now with the hidden decal:

![](../../images/asset-modularity-instancing//hidden-decal.png)

5. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

The trade-off is that we are introducing more total prims by using less instancing. Here's a summarized comparison:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
1 Deinstanced Box | 1741 | 1449 | 3

This is reasonable if you need to make a small amount of targeted edits to instances. It's simple and convenient. If we need to make broader, sweeping changing, then some of the other refinement technique may be better suited.

Let's deinstance another instanceable prim to see how that impacts the stage statistics.

### Deinstancing Multiple Instances

Let's say we needed to make changes to more boxes. Let's apply the same decal {term}`visibility <Visibility>` change to another box.

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

The more we deinstance, the more optimizations we lose. Here's a summarized comparison:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
Instancing | 1711 | 1450 | 3
1 Deinstanced Box | 1741 | 1449 | 3
2 Deinstanced Boxes | 1771 | 1448 | 3

You can see that the complexity scales linearly the more box assets that we deinstance. This will vary though depending on the variety and complexity of the assets you deinstance.

For identical overrides like we've applied on these two boxes, it would be more optimal for OpenUSD to create a new prototype that could be share by the decal-less boxes. In the next units, we will learn about other refinement techniques that do just that.

9. **Close** usdview.

### Conclusion

You've successfully learned deinstancing refinement, the simplest technique for gaining full editability over specific instances. While this approach trades some performance optimization for complete control, you've seen how it enables precise modifications to individual repeated assets when needed, making it ideal for unique cases requiring detailed customization.