# Exercise: Point Instances

## Authoring Point Instances

In this exercise, we will take an export data set of a scatter of boxes and pallets. We'll use this data to create a PointInstancer.

1. **Open** `instancing_exercises/ex_pt_author/author_point_instancer.py` in VSCode to inspect the code.
2. **Run** in the terminal:
```powershell
python .\instancing_exercises\ex_pt_author\author_point_instancer.py
```
3. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_pt_author\Scenario.usd --camera ExCam_01
```

![](../../images/asset-modularity-instancing//point-instancer.png)

4. **Close** usdview.

## Refining Point Instances

In this exercise, we will refine point instances in three ways:
* Deactivating an instance to prune it.
* Promoting an instance to a fully editable asset.
* Using primvars to add shading diversity.

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_pt_refine\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

In the horizontal center of the Viewport, there is a box just in front of a pallet. This is the point that we want to prune. We know ahead of time that this is index 1228 in our PointInstancer arrays.

![](../../images/asset-modularity-instancing//to-prune.png)

2. **Click** *Window > Interpreter* to open the Interpreter window.
3. **Run** the following code in the Interpreter window:
```python
stage = usdviewApi.stage
prim = stage.GetPrimAtPath("/World/Scatter")
pi = UsdGeom.PointInstancer(prim)
pi.DeactivateId(1228)
```

![](../../images/asset-modularity-instancing//box-pruned.png)

You should notice that the box we called out disappeared. This code deactivates the given ID from the PointInstancer. This authors metadata on the PointInstancer that indicates that the given point should be pruned entirely.

What if we didn't want to prune this point, but wanted to promote it instead into a fully editable asset. Promotion starts with pruning, but then you replace the pruned point with the full asset. Let's run some code to reference a new asset and place it in the same place as our pruned point.

4. **Run** the following code in the Interpreter window:
```python
from pathlib import Path
box = stage.DefinePrim("/World/CubeBox_A04_26cm_01")
stage_path = Path(stage.GetRootLayer().identifier)
box_asset_path = stage_path.parent.parent / "src_assets" / "Assets" / "Components" / "CubeBox_A04_26cm" / "CubeBox_A04_26cm.usd"
box.GetReferences().AddReference(str(box_asset_path))
box_xform = UsdGeom.Xformable(box)
box_xform.GetTranslateOp().Set(pi.GetPositionsAttr().Get()[1228])
box_xform.AddOrientOp(precision=UsdGeom.XformOp.PrecisionHalf).Set(pi.GetOrientationsAttr().Get()[1228])
```

The box looks just like it did before in the Viewport, but now we have a new prim hierarchy in the scenegraph where we can author new opinions to manipulate this asset.

![](../../images/asset-modularity-instancing//promotion.png)

Now let's look at a third refinement option using primvars. In this case, we're going to use `primvars:cleanness` to change how clean each of the scattered boxes are.

5. **Run** the following code in the Interpreter window:
```python
import random
pv_api = UsdGeom.PrimvarsAPI(pi)
cleanness = pv_api.CreatePrimvar("cleanness", Sdf.ValueTypeNames.FloatArray, UsdGeom.Tokens.vertex)
cleanness.Set([random.uniform(0.3,1) for x in range(2000)])
```

This code creates `primvars:cleanness` on our PointInstancer, but it uses "vertex" for the variability. What this means is that each item in our array will be assigned to a different PointInstancer point. We're using the `random` library to set 2000 random values.

But nothing changed in the viewport. This is because primvars are inherited, but only if a value hasn't been set by a descendant. The descendant opinion on the prototype that we referenced is stronger than ancestor opinion of the PointInstancer. Fortunately, we can block the prototypes opinion to complete our task.

![](../../images/asset-modularity-instancing//blocking-opinion.png)

6. **Run** the following code in the Interpreter window:
```python
box_proto = stage.GetPrimAtPath("/World/Scatter/Prototypes/CubeBox_A04_26cm")
box_proto.GetAttribute("primvars:cleanness").Block()
```

![](../../images/asset-modularity-instancing//pi-primvar.png)

7. **Close** usdview.