# Exercise: Nested Scenegraph Instancing

## Introduction

In this exercise, you will explore nested instancing by enabling instancing on rack {term}`assemblies <Assembly>` that already contain {term}`components <Component>`. You'll witness dramatic performance improvements while understanding the trade‑offs between optimization and authoring flexibility, learning when nested instancing is most beneficial for complex USD scenes.

## Exercise Steps

### Examine the Current State

Let's start by opening the warehouse scenario where we will be enabling nested instancing. We are starting from a state where the component models are already instanced. Let's confirm this baseline state.

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_nested_inst\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_nested_inst/Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.
3. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected {term}`prim <Prim>` in the Tree View. 

You should see "CubeBox_A04_26cm_18" selected in the Tree View panel. Note the light blue text indicating that we have instancing enabled for our component {term}`assets <Asset>`. In the next steps, we are going to utilize nested instancing and see how that impacts the {term}`stage <Stage>`.

4. **Observe** the decals on the boxes. The boxes with decals showing form a T-shape on the left pallet and the boxes on the right pallet have no decals showing. This visual diversity will be important to observe later.
![](../../images/asset-modularity-instancing/decal-config.png)

5. **Close** usdview.

### Understand the Nested Instancing Script

Let's inspect the script we will be using to author the nested instancing.

6. **Open** `instancing/ex_sg_nested_inst/toggle_nested_inst.py` in VSCode to inspect its code.

```{literalinclude} ../../exercise_content/instancing/ex_sg_nested_inst/toggle_nested_inst.py
:caption: toggle_nested_inst.py
:emphasize-lines: 14-15
:lines: 16-
:lineno-start: 16
:linenos:
```

This script is similar to the script from [Exercise: Author Scenegraph Instancing](./exercise-authoring-scenegraph-instancing.md), but it will enable and disable instancing based on a different criteria.

**Key differences:**
- We are going to use assemblies as our points of interest for authoring scenegraph instancing
- The assemblies contain instanced components to produce the nested instancing we desire
- If you'll recall from [Exercise: Assets Overview](../asset-modularity/exercise-assets-overview.md), we have two assembly assets:
  * BoxPallet_A01
  * Rack_BoxPallet_A01
  
  For the purpose of this exercise, the script will only enable instancing on the racks since BoxPallet_A01 is a part of Rack_BoxPallet_A01. This will give us fewer, but larger prototypes.

```{tip}
Experiment with instancing BoxPallet_A01 instead of Rack_BoxPallet_A01 to see how that impacts the statistics, performance, and authoring flexibility.
```

### Enable Nested Instancing

7. **Run** in the terminal:

Windows:
```powershell
python .\instancing\ex_sg_nested_inst\toggle_nested_inst.py 1
```
Linux:
```sh
python ./instancing/ex_sg_nested_inst/toggle_nested_inst.py 1
```

With the `1` argument, this script now sets all Rack_BoxPallet_A01 assets in `Scenario.usd` to `instanceable=true`. Let's open usdview to see what happened.

8. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_nested_inst\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_nested_inst/Scenario.usd --camera ExCam_01
```

**Observe** that the Rack_BoxPallet_A01 prims are now instances (light blue text).
![](../../images/asset-modularity-instancing/rack-instances.png)

Everything within those Rack_BoxPallet_A01 assets are now instance proxies (dark blue text).

### Analyze the Impact on Stage Statistics

9. **Click** *Window > Interpreter* to open the Interpreter window.
10. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

Scenario | Prims | Instances | Prototypes 
---|---|---|---
No Instancing | 44408 | 0 | 0
Instancing | 1711 | 1450 | 3
Nested Instancing | 1482 | 25 | 1

**Compare the statistics across different instancing strategies:**

**Key observations:**
- The total number of prims has decreased slightly
- The total number of instances is now significantly less (25 vs 1450)
- We only have one prototype based on Rack_BoxPallet_A01

```{admonition} Think About It
What would happen if you disabled instancing for one Rack_BoxPallet_A01? How many prototypes would you have? How many instances?
```

11. **Close** the Interpreter window.

### Observe the Trade-off: Performance vs. Authoring Flexibility

![](../../images/asset-modularity-instancing/local-opinion-lost.png)

**Notice** that every pallet now has the same T-shape formation for box decals. The {term}`stage <Stage>` has lost a significant amount of diversity. A creator painstakingly authored local {term}`opinions <Opinions>` in `Scenario.usd` to give unique positions and rotations to each box for added realism. These local opinions authored on prims within the rack instances are now being ignored.

**This is the key trade-off with nested instancing:** The higher you move your instancing up the {term}`prim hierarchy <Namespace>`, the more performance improvements you gain, but at the cost of authoring flexibility. In later modules, you'll learn techniques to try to balance both of these.

12. **Close** usdview.

### Measure Performance Gains

Let's see those performance gains!

13. **Run** in the terminal:

Windows:
```powershell
Measure-Command { .\scripts\usdview.bat .\instancing\ex_sg_nested_inst\Scenario.usd --quitAfterStartup }
```
Linux:
```sh
time ./scripts/usdview.sh ./instancing/ex_sg_nested_inst/Scenario.usd --quitAfterStartup
```

This will measure how long it takes to execute usdview. usdview is an interactive app, but with the `--quitAfterStartup` flag we can just time the startup and time to first frame with the Storm renderer. You can run the command a few times and take an average for a more reliable result. Our average was 5.31 seconds on a mid-end laptop. Compare the performance results across different instancing strategies:

Scenario | Execution Time (sec) | Improvement (%)
---|---|---
No Instancing | 27.77 | 0% (Baseline)
Instancing | 18.98 | +46.3%
Nested Instancing | 5.31 | +423.0%

The performance gains for leveraging nested instancing where appropriate are undeniable.

## Conclusion

You've successfully implemented nested instancing and achieved remarkable performance gains, improving this content's load and rendering time by 423%. While this optimization comes at the cost of authoring flexibility, you will learn in the next modules how to strategically apply and refine scenegraph instancing to maximize performance in appropriate scenarios.
