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
# Scope 

Understanding scopes is important as they help in organizing and managing complexity in large-scale 3D scenes.

## What is a Scope?

In OpenUSD, a scope is a special type of prim that is used primarily as a grouping mechanism in the scenegraph. It does not represent any geometry or renderable content itself but acts as a container for organizing other prims. Think of scope as an empty folder on your computer where you organize files; similarly, scope helps in structuring and organizing prims within a USD scene.

```{kaltura} 1_ybhfy6qq
```

### How Does It Work?

Scope prims are used to create a logical grouping of related prims, which can be particularly useful in complex scenes with numerous elements. For example, a scope might be used to group all prims related to materials, animation, or geometry. A key feature of scopes is that they cannot be transformed, which promotes their usage as lightweight organizational containers. All
transformable child prims (such as geometry prims or xforms) will be evaluated correctly from within the scope prim and down the hierarchy. This organization aids in simplifying scene management, making it easier for teams to navigate, modify, and render scenes. It also enhances performance by enabling more efficient data management and updates within the scene graph.

### Working With Python

When working with scope in USD using Python, a couple functions are particularly useful:

```python
# Used to define a new scope at a specified path on a given stage
UsdGeom.Scope.Define(stage, path)

# This command is generic, but it's useful to confirm that a prim's type is a scope, ensuring correct usage in scripts
prim.IsA(UsdGeom.Scope)
```

## Examples

### Example 1: Scope and Cube

Other classes that are a part of `UsdGeom` are `Scope` and `Cube`.

[`Scope`](https://openusd.org/release/api/class_usd_geom_scope.html) is a grouping primitive and does NOT have transformability. It can be used to organize libraries with large numbers of entry points. It also is best to group actors and environments under partitioning scopes. Besides navigating, it's easy for a user to deactivate all actors or environments by deactivating the root scope.

[`Cube`](https://openusd.org/release/api/class_usd_geom_cube.html) defines a primitive rectilinear cube centered at the origin.

Similar to how we defined `Xform` above, we can define `Scope` and `Cube` using the same API structure:
- [`UsdGeom.Cube.Define()`](https://openusd.org/release/api/class_usd_geom_cube.html#a77025529a7373c1e74e4f776f282ed8c).
- [`UsdGeom.Scope.Define()`](https://openusd.org/release/api/class_usd_geom_scope.html#acdb17fed396719a9a21294ebca0116ae).

**Add the following code to the cell below, then run the cell:**

```python
# Define a new Xform primitive at the path "/World/Box" on the current stage:
box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))

# Define a new Scope primitive at the path "/World/Box/Geometry" on the current stage:
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))

# Define a new Cube primitive at the path "/World/Box/Geometry/Cube" on the current stage:
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))
```

```{code-cell} ipython3
:cell_id: 581560bdb74e4adeb0a1193020f6c9a3
:deepnote_cell_type: code
:id: SV4FZTCBNDbO

from pxr import Usd, UsdGeom

stage = Usd.Stage.Open("assets/many_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
DisplayUSD("assets/many_prims.usda", show_usd_code=True)
```

## Key Takeaways

Scope prims in OpenUSD play a crucial role in the organization and management of complex 3D scenes. Its primary function is to serve as a container for other prims, helping maintain clarity and structure in large projects.

Next, we'll talk about another way to organize prims: the Xform.



