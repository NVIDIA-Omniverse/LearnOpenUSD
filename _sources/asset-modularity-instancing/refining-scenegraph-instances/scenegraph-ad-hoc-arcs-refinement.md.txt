# Ad Hoc Arcs Refinement

## What Is Ad Hoc Arcs Refinement?

New composition arcs can be added to an instanceable prim on the local layer stack. Within the additional composition arc, you can introduce new opinions on an instance. The result is a new prototype for that instance and any copies that share the new composition arc.

```{figure} ../../images/asset-modularity-instancing/ad-hoc-refinement.png
Composition arcs can be added to introduce ad hoc edits without disabling instancing.
```

In this example, we have four instances of the robot arm. On one of the instanceable prims, we can add a new internal reference with a different pose for the robot arm. The result is three instances using the original prototype and one using the new prototype with an additional internal reference.

The more instances you apply the new composition arc to, the more beneficial and appealing this technique gets. In this example, a dozen or so robot arms using the same pose can make this technique worthwhile.

If you don't foresee a lot of instances leveraging the new ad hoc composition arc, then deinstancing may be a better option and more straight-forward. Don't feel like you have to preserve instancing at all costs. USD has tons of ways to get performance without instancing enabled.

## Exercise: Ad Hoc Arcs Refinement

### Introduction

In this exercise, you will learn ad hoc arcs refinement, a technique that adds new composition arcs to instanceable prims to introduce variety while preserving instancing benefits. You'll add stamps boxes with the word "Damaged" using internal references, observe how this creates new prototypes, and understand when this approach is most beneficial compared to other refinement techniques.

### Exploring the Damaged Stamp Asset

In this exercise, we'll simulate a box that was damaged in the warehouse. We'll add a "Damaged" stamp on a couple of boxes while maintaining instancing enabled for them.

1. **Open** `instancing/src_assets/Assets/Utilities/MiscDecals/MiscDecals.usd` in VSCode to inspect the USDA.

```{literalinclude} ../../exercise_content/instancing/src_assets/Assets/Utilities/MiscDecals/MiscDecals.usd
:caption: MiscDecals.usd
:language: usda
:emphasize-lines: 11
:linenos:
```

`/_MixinOverrides/DamagedStamp` is a speculative `over` (override) that introduces a new decal Mesh and Material for the "Damaged" stamp. This is a bit hard-coded to position the stamp perfectly on the "CubeBox_A04_26cm" asset, but it could be designed to be used more modularly so it could be applied to all sorts of assets. We're going to use this layer as a reference to refine our boxes as an additional ad hoc composition arc.

### Adding Ad Hoc Composition Arcs

2. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_add_arc_refine\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_add_arc_refine/Scenario.usd --camera ExCam_01
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

This code overrides the top first and second boxes on the pallet closest to the camera by adding a new reference to `MiscDecals.usd` on the instanceable prim.

Notice how the top first and second box on the pallet closest to the camera now show a stamp that says, "Damaged".

![](../../images/asset-modularity-instancing/ad-hoc-damaged.png)

### Analyzing the Impact on Stage Statistics

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

**Key observations:**
- The prim count increased by 30 prims (from 1711 to 1741)
- The instance count remained the same (1450)
- A new prototype was created (from 3 to 4 prototypes)
- Because prototypes are built off of composition arcs, introducing a new composition arc to an instance triggers the creation of a new prototype with the modifications that we defined in the new arc
- The new prototype is shared by the two boxes we overrode.

This technique is most beneficial when you have many instances that will use the same ad hoc composition arc.

6. **Close** usdview.

### Conclusion

You've successfully learned ad hoc arcs refinement, a technique that adds new composition arcs to instanceable prims to introduce variety while preserving instancing benefits. This approach is most effective when you have multiple instances that will share the same override, as it creates new prototypes that can be reused efficiently across similar instances.