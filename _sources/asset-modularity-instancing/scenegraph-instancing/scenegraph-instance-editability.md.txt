# Instance Editability

Prototypes are a runtime data model and are **not editable**.
Instance proxies are **not editable**. Local opinions are discarded.
Instanceable prims are **editable**.

``` usda

#usda 1.0

(
    defaultPrim = "World"
    metersPerUnit = 0.01    
    upAxis = "Z"
)
def Xform "World"
{
    def "RobotArm_01" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
        double3 xformOp:translate = (10, 0, 20)        
        over "joint_1" {
            double3 xformOp:rotateX = 10        
        }
    }
}
over "__Prototype_01" {
    color3f primvars:asset_color = [(1, 0, 0)]
}

```

## Exercise: Instance Editability

### Immutability of Instance Proxies

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_editability\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box closest to the camera in the Viewport.

![](../../images/asset-modularity-instancing//top-left-box-closeup.png)

3. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected prim in the Tree View.

You should see "CubeBox_A04_26cm_18" selected in the Tree View panel.

4. **Click** the triangle to the left of the select prim in the Tree View to expand the select prim's hierarchy.
5. **Click** on "SM_CubeBox_A04_Decal_01" that was revealed in the Tree View.

We've decided that this box should not have any decals. We want to hide the decals on this box. This is an instance proxy though as denoted by the dark blue text. We'll see what happens when we try to author this change.

6. In the Property panel, **click** on the "visibility" attribute.

![](../../images/asset-modularity-instancing//select-vis.png)
We'll use this property selection in subsequent steps to try to hide the decal.

7. **Click** *Window > Interpreter* to open the Interpreter window.
8. **Run** the following code in the Interpreter window:
```python
vis = usdviewApi.property
vis.Set(UsdGeom.Tokens.invisible)
```

You should see an error like this in the Interpreter window:

```shell
Traceback (most recent call last):
  File "<input>", line 1, in <module>
pxr.Tf.ErrorException: 
	Error in 'pxrInternal_v0_25_5__pxrReserved__::UsdStage::_ValidateEditPrim' at line 1504 in file C:\g\163073426\USD\pxr\usd\usd\stage.cpp : 'Cannot create property spec at path </World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_18/SM_CubeBox_A04_Decal_01>; authoring to an instance proxy is not allowed.'
	Error in 'pxrInternal_v0_25_5__pxrReserved__::UsdStage::_SetValueImpl' at line 7102 in file C:\g\163073426\USD\pxr\usd\usd\stage.cpp : 'Cannot set attribute value.  Failed to create attribute spec </World/Warehouse/Rack_BoxPallet_A01_01/BoxPallet_A01_03/CubeBox_A04_26cm_18/SM_CubeBox_A04_Decal_01.visibility> in layer @anon:0000020B75F5EAE0@'
```

The decal prim is a instance proxy which makes it immutable. OpenUSD outputs an error explaining that we can't author a local opinion to change the visibility of the decal prim.

Instances are not entirely immutable though. Instance prims (i.e. the root prim of an instance) can be edited. This is what allows scenegraph instances to have unique transformations in the scene. Let's look at how instance prims can be mutated.

### Mutability of Instance Prims

9. **Click** on "CubeBox_A04_26cm_18" in the Tree View.
10. In the Property panel, **click** on the "xformOp:translate" attribute.

![](../../images/asset-modularity-instancing//select-translate.png)

11. **Run** the following code in the Interpreter window:
```python
translate = usdviewApi.property
x, y, z = translate.Get()
translate.Set((x, y, z+20.0))
```

![](../../images/asset-modularity-instancing//instance-prim-tranlsation.png)

Note how the box moved up 20 units in the viewport and it didn't produce any errors.

This component-based instancing scheme enables us to benefit from instancing, but we can still perform tasks like removing and moving instanced boxes within our shipping and receiving warehouse. You can author other opinions on the instance prim to control things like visibility or activation of a prim.

12. **Close** usdview.

## Refining Scenegraph Instancing

![](../../images/asset-modularity-instancing/slides/Slide39.jpg)

Instances cannot be directly refined on the local layer stack
Options for downstream refinement:
* Deinstancing
* Hierarchical Refinement
    * Transformation Operations (xformOps)
    * Primvars
* Composition Arcs
    * Variant Selection
    * Ad Hoc Internal References
    * Broadcasted Inherits and Specializes
