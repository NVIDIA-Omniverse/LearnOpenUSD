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
# XformCommonAPI

## What is XformCommonAPI?
`XformCommonAPI ` is a component of the OpenUSD framework. Today, we're diving into this API to understand its utility in the 3D content creation pipeline.

This API facilitates the authoring and retrieval of a common set of operations with a single translation, rotation, scale and pivot that is generally compatible with import and export into many tools. It's designed to simplify the interchange of these transformations.

```{kaltura} 1_tx9y8k5c
```

### How Does It Work?

The API provides methods to get and set these transformations at specific times--for instance, it allows the retrieval of transformation vectors at any
given frame or TimeCode, ensuring precise control over the simulation process.

There’s another way to author and retrieve translations – through the `UsdGeomXformable` function. Xformable prims support arbitrary sequences of transformations, which gives power users a lot of flexibility. A user could
place two rotations on a “Planet” prim, allowing them to control revolution and rotation around two different pivots on the same prim. This is powerful, but complicates simple queries like “What is the position of an object at time 101.0?”

### Working With Python

Below is an example of how to work with the `XformCommonAPI` in a USD environment.

```python
from pxr import Usd, UsdGeom

# Create a stage and define a prim path
stage = Usd.Stage.CreateNew('example.usda')
prim = UsdGeom.Xform.Define(stage,'/ExamplePrim')

# Check if the XformCommonAPI is compatible with the prim using the bool operator 
if not (xform_api := UsdGeom.XformCommonAPI(prim)):
    raise Exception("Prim not compatible with XformCommonAPI")
```

These commands demonstrate how to apply translations, rotations, and scaling to a 3D object using the `XformCommonAPI`. We can get a transformation matrix
from the xformable prim that works with any `xformOp` order using the [`GetLocalTransformation`](https://openusd.org/release/api/class_usd_geom_xformable.html#a9a04ccb1ba8aa16e8cc1e878c2c92969) method.

## Examples

## Example 1: 

 To view more, look at [`UsdGeomCube`'s](https://openusd.org/release/api/class_usd_geom_cube.html#pub-methods) public member functions. The function names typically end with *Attr*. 

Let's look into setting another attribute and how we can get the value from an attribute.

+++ {"cell_id": "a2458273d57e4c748cc9e4e741679b8f", "deepnote_cell_type": "markdown"}

**Add the following code to the cell below, then run the cell:**
   
```python
# Get the Cube's `size` attribute:
cube_size_attr: Usd.Attribute = cube.GetSizeAttr()
# Get the value of the Cube's `Size` attribute, double it and set it as the new value for the `Size` attribute:
cube_size_attr.Set(cube_size_attr.Get() * 2)
# Get the prim at the path: `/Geometry/GroupTransform`:
geom_scope: UsdGeom.Scope = stage.GetPrimAtPath("/Geometry/GroupTransform")
# Define a Cube Prim in stage as a child of geom_scope called `Small_Box`:
small_box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath("Small_Box"))
# Set the position of the `small_box` to x: 4, y: 5, z: 4
UsdGeom.XformCommonAPI(small_box).SetTranslate((4, 5, 4))
```

```{code-cell} ipython3
:cell_id: 58f248e2ba654f0f9da1b69344b7d580
:deepnote_cell_type: code
:deepnote_to_be_reexecuted: false
:execution_millis: 197
:execution_start: 1715975968664
:source_hash: null

from pxr import Usd, UsdGeom

file_path = "assets/second_stage.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

cube: UsdGeom.Cube = UsdGeom.Cube(stage.GetPrimAtPath("/Geometry/GroupTransform/Box"))
cube_color_attr: Usd.Attribute = cube.GetDisplayColorAttr()
cube_color_attr.Set([(1.0, 0.0, 0.0)])

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()
DisplayUSD(file_path, show_usd_code=True)
```

+++ {"cell_id": "446339e0c22741e3a057d3a37c01ae27", "deepnote_cell_type": "markdown"}

Here we used `GetSizeAttr()` to retrieve the attribute that defines the size of the cube. This is also a public member function defined in `UsdGeomCube`. To get the value of an attribute we use [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9). Each [`UsdAttribute`](https://openusd.org/release/api/class_usd_attribute.html) contains a `Set()` and `Get()` function for its values. 

[`XformCommonAPI`](https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html) is used to set and get transform components such as scale, rotation, scale-rotate pivot and translation. Even though these are considered attributes, it is best to go through `XformCommonAPI` when editting transformation values. `XformCommonAPI` is a great way to bootstrap setting up new transformations. Future courses will dive into advanced usage of xformOps. Below is an example to check if `XformCommonAPI` is compatible with the prim.


``` python 
from pxr import Usd, UsdGeom

# Create a stage and define a prim path
stage = Usd.Stage.CreateNew('example.usda')
prim = UsdGeom.Xform.Define(stage, '/ExamplePrim')

# Check if the XformCommonAPI is compatible with the prim using the bool operator 
if not (xform_api := UsdGeom.XformCommonAPI(prim)):
    raise Exception("Prim not compatible with XformCommonAPI")

# Set transformations
xform_api.SetTranslate((10.0, 20.0, 30.0))
xform_api.SetRotate((45.0, 0.0, 90.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)
xform_api.SetScale((2.0, 2.0, 2.0))

```

## Key Takeaways

The `XformCommonAPI` provides the preferred way for authoring and retrieving a standard set of component transformations, including scale, rotation, scale-
rotate pivot and translation.

The goal of the API is to enhance, reconfigure or adapt each structure without changing the entire system. This approach allows for flexibility and customization by focusing on the individual parts rather than the whole. This is done by limiting the set of allowed basic operations and by specifying the order in which they are applied.
