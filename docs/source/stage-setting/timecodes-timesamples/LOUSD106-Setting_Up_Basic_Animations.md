---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: .venv
  language: python
  name: python3
---

+++ {"cell_id": "6ff4912e957a48d5ae7e73349ffa626c", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

# **Learn OpenUSD: Setting Up Basic Animations**

Welcome to the Jupyter notebook for *Learn OpenUSD: Setting Up Basic Animations*. This is where we will find all the Python activities related to this course. Before starting **Activity 1**, make sure to run the cell below.

+++ {"cell_id": "f8fb46fe73394683bd5f07f9aac99f01", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.

```{code-cell} ipython3

from utils.visualization import DisplayUSD
from utils.helperfunctions import create_new_stage
```

+++ {"cell_id": "19ea3760a3cf4828a790686be96def08", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

Let's also create a USD stage to use for this module, using the [`Stage`](https://openusd.org/release/glossary.html#usdglossary-stage) class from the `Usd` module.

**Run the cell below to create a new USD Stage:**

```{code-cell} ipython3
:cell_id: 6f38122a48364ab58825190594bb39c6
:deepnote_cell_type: code
:deepnote_to_be_reexecuted: false
:execution_millis: 24
:execution_start: 1716331247240
:source_hash: null

# Import the necessary modules from the `pxr` library:
from pxr import Usd, UsdGeom, Gf

# Create a new USD stage file named "timecode_sample.usda":
stage: Usd.Stage = create_new_stage("assets/timecode_sample.usda")

# Define a transform ("Xform") primitive at the "/World" path:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a Sphere primitive as a child of the transform at "/World/Sphere" path:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# Define a blue Cube as a background prim:
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# Save the stage to the file:
stage.Save()
DisplayUSD("assets/timecode_sample.usda", show_usd_code=True)
```

+++ {"cell_id": "07e7bbec4fe542e6a4aa2c9da60dd73f", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

---

## **Activity 1**: Setting TimeCodes

[`TimeCode`](https://openusd.org/release/glossary.html#usdglossary-timecode) specifies an exact frame or moment in the animation timeline. It allows for precise control over the timing of changes to properties, enabling smooth and accurate animation of 3D objects. 

A [`Usd.TimeCode`](https://openusd.org/release/api/class_usd_time_code.html) is therefore a unitless, generic time measurement that serves as the ordinate for time-sampled data in USD files. [`Usd.Stage`](https://openusd.org/release/api/class_usd_stage.html) defines the mapping of `TimeCode`s to units like seconds and frames.

To set the stage's `start` TimeCode and `end` TimeCode, use the [`SetStartTimeCode()`](https://openusd.org/release/api/class_usd_stage.html#aef35e121cd9662129b6e338e85ceab44) and [`SetEndTimeCode()`](https://openusd.org/release/api/class_usd_stage.html#a05e5e8a51041bc7f9b7f1165ccec9fa4) methods.

+++

**Add the following code to the cell below, then run the cell to set the start and end TimeCodes for the stage:**

``` python
# Set the `start` and `end` timecodes for the stage:
stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)
```

```{code-cell} ipython3
:cell_id: 9f31cf6c56814d3a93c6fa3a06a0a189
:deepnote_cell_type: code

from pxr import Usd, UsdGeom, Gf

stage: Usd.Stage = Usd.Stage.Open("assets/timecode_sample.usda")
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Set the `start` and `end` timecodes for the stage:
stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()
DisplayUSD("assets/timecode_sample.usda", show_usd_code=True)
```

+++ {"cell_id": "a72cd09e55524957a50a2da263acbcb0", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

---

## **Activity 2**: Setting TimeCode and Values for Attributes

[TimeSamples](https://openusd.org/release/glossary.html#usdglossary-timesample) represent a collection of attribute values at various points in time, allowing OpenUSD to interpolate between these values for animation purposes.

When animating an attribute, you define a timeCode at which the value should be applied. These values are then interpolated between the timeSamples to get the value that should be applied at the current [timeCode](https://openusd.org/release/glossary.html#usdglossary-timecode).

To assign a value at a particular timeCode, use the [`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a7fd0957eecddb7cfcd222cccd51e23e6) method. 

[`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a7fd0957eecddb7cfcd222cccd51e23e6) takes two arguments: the timeCode and the value to assign.

For example, if you want to set the size of a cube to `1` at timeCode `1` and `10` at timeCode `60`:

```python
# Get the size attribute of the cube
cube_size_attr: Usd.Attribute = cube_prim.GetSizeAttr()
# Set the size of the cube at time=1 to 1
cube_size_attr.Set(time=1, value=1)
# Set the size of the cube at time=60 to 10
cube_size_attr.Set(time=60, value=10)
```

TimeSamples are then created for the cube's size attribute between timeCodes.

+++

Let's create a sphere that moves up and down using the [`XformCommonAPI`](https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html).

**Add the following code to the cell below, then run the cell:**

```python
# Create XformCommonAPI object for the sphere
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

# Set translation of the sphere at time 1
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)  
# Set translation of the sphere at time 30
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)  
# Set translation of the sphere at time 45
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)  
# Set translation of the sphere at time 50
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)  
# Set translation of the sphere at time 60
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)  
```

```{code-cell} ipython3
:allow_embed: false
:cell_id: fdacf81521ab483f9a11b897fc7b39d3
:deepnote_cell_type: code

from pxr import Usd, UsdGeom

stage: Usd.Stage = Usd.Stage.Open("assets/timecode_sample.usda")
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)

# Grab the translate 
if translate_attr := sphere.GetTranslateOp().GetAttr():
    translate_attr.Clear()

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Create XformCommonAPI object for the sphere
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

# Set translation of the sphere at time 1
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)  
# Set translation of the sphere at time 30
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)  
# Set translation of the sphere at time 45
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)  
# Set translation of the sphere at time 50
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)  
# Set translation of the sphere at time 60
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
DisplayUSD("assets/timecode_sample.usda", show_usd_code=True)
```

+++ {"cell_id": "dafc4cc776cf4a0c99a93d1dc998d8bd", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}


[TimeSamples](https://openusd.org/release/glossary.html#usdglossary-timesample) are used for baked animation that are linear and it is good for interchange that is reproducible. However, [timeSamples](https://openusd.org/release/glossary.html#usdglossary-timesample) are not a replacement for animation curves.

For more complex animation it is not recommended to define the animation using scripting but rather in other Digital Content Creation (DCC) Applications.

+++

It is possible to set multiple values at multiple timeCodes. We can demonstrate this with the scale of the sphere. It is advisable to create a [timeCode](https://openusd.org/release/glossary.html#usdglossary-timecode) for each instance we created for "translate", and we will apply the same approach for "scale".

**Add the following code to the cell below, then run the cell:**

```python
# Set scale of the sphere at time 1
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=1)  
# Set scale of the sphere at time 30
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=30)   
# Set scale of the sphere at time 45
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 0.20, 1.25), time=45)   
# Set scale of the sphere at time 50
sphere_xform_api.SetScale(Gf.Vec3f(0.75, 2.00, 0.75), time=50)  
# Set scale of the sphere at time 60
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=60)  
```

```{code-cell} ipython3
:cell_id: 71a2eeecbc554e08a153ddc37c1e4c4d
:deepnote_cell_type: code

from pxr import Usd, UsdGeom

stage: Usd.Stage = Usd.Stage.Open("assets/timecode_sample.usda")
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)

if translate_attr := sphere.GetTranslateOp().GetAttr():
    translate_attr.Clear()
if scale_attr := sphere.GetScaleOp().GetAttr():
    scale_attr.Clear()

sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)  

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Set scale of the sphere at time 1
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=1)  
# Set scale of the sphere at time 30
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=30)   
# Set scale of the sphere at time 45
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 0.20, 1.25), time=45)   
# Set scale of the sphere at time 50
sphere_xform_api.SetScale(Gf.Vec3f(0.75, 2.00, 0.75), time=50)  
# Set scale of the sphere at time 60
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=60)  

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
DisplayUSD("assets/timecode_sample.usda", show_usd_code=True)
```
