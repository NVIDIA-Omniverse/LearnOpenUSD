# Refining Point Instances

## Refinement Using Primvars

{term}`Primvars <Primvar>` using `vertex` interpolation will be applied per instance. Like scenegraph instancing, you can introduce a lot of diversity in your point instances by using prototypes that read primvars.

In the case of our packing peanut example, our packing peanut {term}`asset <Asset>`'s material network may read from a `primvars:peanut_color` primvar. Authoring this primvar on our PointInstancer could enable us to make each peanut a different color if we wanted to.
```{code-block} usda

#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 0.01    
    upAxis = "Z"
)
over "PackingPeanuts"
{
    color3f[] primvars:peanut_color = [...](
        interpolation = "vertex"
    )
}
```

## Introducing New Prototypes

If you want to introduce more variety into a PointInstancer with additional prototypes, point instancing's explicit prototype pattern requires a bit more work than scenegraph instancing. You will need to:

1. Define an additional {term}`prim hierarchy <Namespace>` for the new prototype.
2. Add the new prototype to the `prototypes` {term}`relationship <Relationship>`.
3. Update `protoIndices` to specify which instances should use the new prototype.

## Refinement Using Visibility and Deactivation

At any point downstream, you can refine your PointInstancer by pruning or hiding instances using `inactiveIds` {term}`metadata <Metadata>` and `invisibleIds` {term}`attribute <Attribute>` respectively.

```{figure} ../images/asset-modularity-instancing/inactiveids.mp4
Deactivating packing peanuts that fell out of the box after the physics simulation process.
```

A good rule of thumb is that if you need to animate an instance on and off over time, you should use `invisibleIds`, otherwise, use `inactiveIds`. A nice feature of `inactiveIds` is that it can be list-edited so you can sparsely add and remove ids.

## Refinement Using Promotion

Promotion in this case is what we call turning a point instance into a full-fledged subgraph on the {term}`stage <Stage>` so you can override it more intuitively.

```{figure} ../images/asset-modularity-instancing/point-instance-promotion.mp4
Promoting a point instance.
```
In this example, maybe we're creating a commercial and we want to turn a packing peanut into an animated character. We can use `inactiveIds` to deactivate the point instance that will be replaced by the character and then {term}`reference <Reference>` the character into the same position. Now we can animate and override the referenced character as we see fit.

## Exercise: Refining Point Instances

### Introduction

In this exercise, you will learn three key techniques for refining point instances: deactivating instances to prune them, promoting instances to fully editable assets, and using primvars to add shading diversity. You'll explore how these techniques allow you to introduce variety and control into your PointInstancer while maintaining performance benefits, giving you the flexibility to customize individual instances when needed.

### Exploring the Point Instancer Scenario

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_pt_refine\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_pt_refine/Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

In the horizontal center of the Viewport, there is a box just in front of a pallet. This is the point that we want to prune. We know ahead of time that this is index `1228` in our PointInstancer arrays.

![](../images/asset-modularity-instancing/to-prune.png)

### Deactivating Point Instances

2. **Click** *Window > Interpreter* to open the Interpreter window.
3. **Run** the following code in the Interpreter window:
```python
stage = usdviewApi.stage
prim = stage.GetPrimAtPath("/World/Scatter")
pi = UsdGeom.PointInstancer(prim)
pi.DeactivateId(1228)
```

![](../images/asset-modularity-instancing/box-pruned.png)

You should notice that the box we called out disappeared. This code deactivates the given ID from the PointInstancer. This authors metadata on the PointInstancer that indicates that the given point should be pruned entirely.

### Promoting Point Instances

What if we didn't want to prune this point, but wanted to promote it instead into a fully editable asset. Promotion starts with pruning, but then you replace the pruned point with the full asset. Let's run some code to {term}`reference <Reference>` a new asset and place it in the same place as our pruned point. We will continue with point `1228` for this part.

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

The box looks just like it did before in the Viewport, but now we have a new prim hierarchy in the scenegraph where we can author new {term}`opinions <Opinions>` to manipulate this asset.

![](../images/asset-modularity-instancing/promotion.png)

### Using Primvars for Shading Diversity

Now let's look at a third refinement option using primvars. In this case, we're going to use `primvars:cleanness` this is a custom primvar that we created for the CubeBox_A04_26cm asset ahead of time. It's the same primvar used for [Exercise: Hierarchical Refinement Using Primvars](./refining-scenegraph-instances/scenegraph-hierarchical-refinement.md#exercise-hierarchical-refinement-using-primvars) to change how clean a box appears.

5. **Run** the following code in the Interpreter window:
```python
import random
pv_api = UsdGeom.PrimvarsAPI(pi)
cleanness = pv_api.CreatePrimvar("cleanness", Sdf.ValueTypeNames.FloatArray, UsdGeom.Tokens.vertex)
cleanness.Set([random.uniform(0.3,1) for x in range(2000)])
```

This code creates `primvars:cleanness` on our PointInstancer, but it uses "vertex" for the variability. What this means is that each item in our array will be assigned to a different PointInstancer point. We're using the `random` library to set 2000 random values.

But nothing changed in the viewport. This is because primvars are inherited, but only if a value hasn't been set by a descendant. The descendant opinion on the prototype that we referenced is stronger than ancestor opinion of the PointInstancer. 

* World
  * Scatter (weaker)
    * Prototypes
      * CubeBox_A04_26cm (stronger)

Fortunately, we can block the prototype's opinion to complete our task.

![](../images/asset-modularity-instancing/blocking-opinion.png)

6. **Run** the following code in the Interpreter window:
```python
box_proto = stage.GetPrimAtPath("/World/Scatter/Prototypes/CubeBox_A04_26cm")
box_proto.GetAttribute("primvars:cleanness").Block()
```

![](../images/asset-modularity-instancing/pi-primvar.png)

Now you should see the varying degrees of dirtiness on the scattered boxes.

7. **Close** usdview.

### Conclusion

You've successfully learned three key techniques for refining point instances: deactivating instances to prune them, promoting instances to fully editable assets, and using primvars to add shading diversity. These techniques give you the flexibility to customize individual instances when needed while maintaining the performance benefits of PointInstancer, making it an ideal solution for large-scale scenes that require both efficiency and control.