# Hierarchical Refinement

## What Is Hierarchical Refinement?

Hierarchical refinement refers to the process of refining instances by authoring inherited properties on ancestor prims. The most common inherited properties used for this type of refinement are:

* **Transformation Operations (xformOps)** – Moving, rotating, or scaling an ancestor prim will affect all of its descendant instances.
* **Visibility** – Making an ancestor invisible will also hide all of its descendant instances.
* **Primvars** – Assigning primvar values to an ancestor can create shading or material variations among its descendant instances.

Importantly, these refinements do not create any new prototypes; they simply leverage inheritance to efficiently introduce variety or control across instances.

## Hierarchical Refinement Using Primvars

Primvars are a way you can drive material properties like color, but it's not limited to just that. The convenient feature about primvars is that they inherit down the prim hierarchy. What this means is that you can set an opinion for a primvar on the instanceable prim (or any ancestor) and your materials can read that inherited value at any point in an instance's subgraph. You can use primvars to hierarchically refine instances.

This form of refinement does not introduce any new prototypes since the subgraphs among the instances remain identical. The only new opinions are found on the instanceable prims. This makes primvars a very lightweight way to introduce a ton of variety in a scene with very little performance implications.

Let's look at a concrete example of hierarchical refinement using primvars.

```{code-block} usda
:emphasize-lines: 14-16,30-32
:linenos:

#usda 1.0
(
    defaultPrim = "Warehouse"
    metersPerUnit = 0.01
    upAxis = "Z"
)
def Xform "Warehouse"
{
    def "RobotArm_01" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
        color3f[] primvars:arm_color = [(0.61, 0.75, 0.24)] (
            interpolation = "constant"
        )
    }
    def "RobotArm_02" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
    }
    def "RobotArm_03" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
        color3f[] primvars:arm_color = [(0.08, 0.70, 0.52)] (
            interpolation = "constant"
        )
    }
    
}
```

```{figure} ../../images/asset-modularity-instancing/primvar-refinement.png
Three unique robot arms all sharing one prototype.
```

In this example, we are setting `primvars:arm_color` on the instanceable prim to change the color of two robot arms. The `RobotArm.usd` asset has a shader to read this value and use it within its material network.

## Exercise: Hierarchical Refinement Using Primvars

### Introduction

In this exercise, you will learn hierarchical refinement using primvars, an efficient refinement technique that introduces variety without creating new prototypes. You'll use a custom "cleanness" primvar to control material appearance, observe how primvars inherit through the prim hierarchy, and understand why this approach has minimal performance impact while enabling extensive visual variety.

### Understanding the Custom Primvar

In this exercise, we're going to use a custom "cleanness" primvar that we authored for our box asset to control the brightness of the box's cardboard material. In simulation, we could use this as a visual representation of how long a box has been in the warehouse. An older box would appear dirtier or darker than the rest. This would enable us to quickly scan our digital twin and find boxes that have been sitting around for a long time.

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_primvar_refine\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_primvar_refine/Scenario.usd --camera ExCam_01
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

This shader is used by all boxes to check for `primvars:cleanness` on any gprim (e.g. Mesh or Subset) that it's assigned to.

8. **Click** on "UsdPreviewSurface" to select it.
9. **Click** on the triangle to the left of the "inputs:occlusion" attribute in the Property panel expand it.

![](../../images/asset-modularity-instancing//occlusion.png)

This reveals that the output from "UsdPrimvarReader_cleanness" is connected to "inputs:occlusion" to drive the occlusion of this cardboard material. The closer the number gets to `0.0`, the darker the material gets.

### Setting Primvar Values

Let's see the custom primvar in action on our instanced boxes.

10. **Click** *Window > Interpreter* to open the Interpreter window.
11. **Run** the following code in the Interpreter window:
```python
stage = usdviewApi.stage
box1 = stage.GetPrimAtPath("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_18")
box2 = stage.GetPrimAtPath("/World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_17")
box1.GetAttribute("primvars:cleanness").Set([0.8])
box2.GetAttribute("primvars:cleanness").Set([0.6])
```

Note how the two boxes closest to the camera are now darker from the rest.
![](../../images/asset-modularity-instancing//cleanness-set.png)

### Analyzing the Impact Using Stage Statistics

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

**Key observations:**
- Primvar refinement does not add any prims to the total prim count
- All we are doing is authoring a new opinion on the instanceable prims that are already a part of the total prim count
- No new prototypes are created either
- The single prototype handles all of the shading variability on its own

This makes primvars a very efficient refinement technique for introducing visual variety.

13. **Close** usdview.

### Conclusion

You've successfully leveraged hierarchical refinement using primvars, an efficient technique for introducing variety into instanced scenes. By leveraging primvars and material networks, you can create extensive visual diversity without any performance penalty, making this approach ideal for large-scale scenes requiring subtle variations.