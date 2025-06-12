---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---
# Materials and Shaders

## What is a Material?

### How Does It Work?

### Working With Python

## Examples

### Example 1: UsdShade and Material

[`UsdShade`](https://openusd.org/release/api/usd_shade_page_front.html) is a schema for creating and binding materials.

[`Material`](https://openusd.org/release/api/class_usd_shade_material.html) provides a container to store data for defining a "shading material" to a renderer.

`UsdShade` and `Materials` will be covered in later topics and are only covered here to show another use case for schema-specific APIs.

**Add the following code to the cell below, then run the cell:**

```python
# Define a new Scope primitive at the path "/World/Box/Materials" on the current stage:
mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))

# Define a new Material primitive at the path "/World/Box/Materials/BoxMat" on the current stage:
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))
```

> **NOTE:** The material is not applied to the cube so it will not show up in the scene visually, but it is displayed in the hierarchy.

```{code-cell} ipython3
:cell_id: 6b923060dcb648f49f41a9f1f9545650
:deepnote_cell_type: code
:id: 5UsGOdLYNDbO

from pxr import Usd, UsdGeom, UsdShade

stage: Usd.Stage = Usd.Stage.Open("assets/many_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
DisplayUSD("assets/many_prims.usda", show_usd_code=True)
```


## Key Takeaways