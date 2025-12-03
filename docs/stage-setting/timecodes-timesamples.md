---
# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

kernelspec:
  name: python3
  display_name: python3
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.13'
    jupytext_version: 1.17.2
---

# Time Codes and Time Samples


This lesson, _Time Code and Time Sample_, shows us how to set up animation in a {term}`stage <Stage>` using OpenUSD.

In this lesson, we will:

  * **Set start and end time codes for a stage**. Learn how to set start and end time code metadata for a USD stage, establishing a timeline that forms the foundation for animated scenes.
  * **Set time samples on {term}`attributes <Attribute>`**. Gain the skills to set time samples on individual attributes, allowing us to animate specific properties of {term}`prims <Prim>` over time.

## What are Time Codes and Time Samples?

![Time Code Time Sample Definition](../images/foundations/TimeCodeTimeSample_Definition.webm)

In OpenUSD, {term}`time code <Time Code>` and {term}`time sample <Time Sample>` are two important concepts that enable us
to work with animations and simulation in USD scenes.

Time code is a point in time with no unit assigned to it. You can think of
these as frames whose units are derived from the stage.

Time sample refers to the individual time-varying values associated with an
attribute in USD. Each attribute can have a collection of time samples that map
time code to the attribute's data type values, allowing for animation over
time. For a reminder of the purpose of attributes, please review the introductory {doc}`lesson on attributes <properties/attributes>`.

### How Does It Work?

In a USD scene, the time code ordinates of all time samples are scaled to
seconds based on the `timeCodesPerSecond` {term}`metadata <Metadata>` value defined in the root {term}`layer <Layer>`.

This allows flexibility in encoding time samples within a range and scale
suitable for the application, while maintaining a robust mapping to real-world
time for playback and decoding.

For example, if the root layer has `timeCodesPerSecond=24`, a time code value
of `48.0` would correspond to 2 seconds (48/24) of real time after the
time code `0`.

Time samples are used to store time-varying data for attributes, such as
positions, rotations, or material properties. When an attribute is evaluated
at a specific time code, the value is linearly interpolated from the
surrounding time samples, allowing for smooth animation playback.

### Working With Python

![Time Code Time Sample Python](../images/foundations/TimeCodeTimeSample_Python.webm)

Below is an example of how we can get or set time samples in Python. First,
we're getting the time samples of the `displayColor` on a cube prim. This
method returns a vector of time code ordinates at which time samples are
authored for the given attribute.

Lastly, we're setting a translation value of a sphere at a specified time code.
This method sets the time sample value of the attribute at the specified
time code.

```python
# Returns authored time samples
cube.GetDisplayColorAttr().GetTimeSamples()

# Sets time sample Value (Gf.Vec3d(0,-4.5,0)) at a specified TimeCode (30)
sphere_xform_api.SetTranslate(Gf.Vec3d(0,-4.5,0), time=Usd.TimeCode(30))
```

## Examples
+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD
from utils.helperfunctions import create_new_stage
```

Let's create a USD stage to serve as the starting point for the example in this lesson. We will create a simple stage with a sphere and a blue cube as a backdrop.

```{code-cell}
:tags: [remove-output]
# Import the necessary modules from the `pxr` library:
from pxr import Usd, UsdGeom, Gf

# Create a new USD stage file named "timecode_sample.usda":
file_path = "_assets/timecode_sample.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

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
```
```{code-cell}
:tags: [remove-input]
DisplayUSD("_assets/timecode_sample.usda", show_usd_code=True)
```

### Example 1: Setting Start and End Time Codes

Time code specifies an exact frame or moment in the animation timeline. It allows for precise control over the timing of changes to properties, enabling smooth and accurate animation of 3D objects. 

A [`Usd.TimeCode`](https://openusd.org/release/api/class_usd_time_code.html) is therefore a unitless, generic time measurement that serves as the ordinate for time-sampled data in USD files. [`Usd.Stage`](https://openusd.org/release/api/class_usd_stage.html) defines the mapping of time codes to units like seconds and frames.

To set the stage's `startTimeCode` and `endTimeCode` metadata, use the [`SetStartTimeCode()`](https://openusd.org/release/api/class_usd_stage.html#aef35e121cd9662129b6e338e85ceab44) and [`SetEndTimeCode()`](https://openusd.org/release/api/class_usd_stage.html#a05e5e8a51041bc7f9b7f1165ccec9fa4) methods.

```{code-cell}
:tags: [remove-output]
:emphasize-lines: 6-8

from pxr import Usd

# Open stage from starting point usda
stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_sample.usda")

# Set the `start` and `end` time codes for the stage:
stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)

# Export to a new flattened layer for this example.
stage.Export("_assets/timecode_ex1.usda", addSourceFileComment=False)
```
Note the stage metadata at the top of the layer.
```{code-cell}
:tags: [remove-input]
DisplayUSD("_assets/timecode_ex1.usda", show_usd_code=True)
```


### Example 2: Setting Time Samples for Attributes

Time samples represent a collection of attribute values at various points in time, allowing OpenUSD to interpolate between these values for animation purposes.

When animating an attribute, you define a time code at which the value should be applied. These values are then interpolated between the time samples to get the value that should be applied at the current time code.

To assign a value at a particular time code, use the [`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a7fd0957eecddb7cfcd222cccd51e23e6) method. 

[`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a7fd0957eecddb7cfcd222cccd51e23e6) takes two arguments: the time code and the value to assign.

For example, if you want to set the size of a cube to `1` at time code `1` and `10` at time code `60`:

```python
# Get the size attribute of the cube
cube_size_attr: Usd.Attribute = cube_prim.GetSizeAttr()
# Set the size of the cube at time=1 to 1
cube_size_attr.Set(time=1, value=1)
# Set the size of the cube at time=60 to 10
cube_size_attr.Set(time=60, value=10)
```

USD will interpolate the values for the cube's size attribute between set time samples.

Let's create a sphere that moves up and down using the [`XformCommonAPI`](https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html).

```{code-cell}
:tags: [remove-output]
:emphasize-lines: 8-24

from pxr import Usd, UsdGeom, Gf

# Open stage from example 1
stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_ex1.usda")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Sphere")

# Clear any existing translation
if translate_attr := sphere.GetTranslateOp().GetAttr():
    translate_attr.Clear()

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

# Export to a new flattened layer for this example.
stage.Export("_assets/timecode_ex2a.usda", addSourceFileComment=False)
```
```{code-cell}
:tags: [remove-input]
DisplayUSD("_assets/timecode_ex2a.usda", show_usd_code=True)
```

Time samples can be used for baked, per-frame animation and it is good for interchange that is reproducible. However, time samples are not a replacement for animation curves.

For more complex animation it is not recommended to define the animation using scripting but rather in other Digital Content Creation (DCC) Applications.

---

It is possible to set time samples for different attributes. We can demonstrate this with the scale of the sphere.

```{code-cell}
:tags: [remove-output]
:emphasize-lines: 8-22

from pxr import Usd, UsdGeom, Gf

# Open stage from example 2a
stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_ex2a.usda")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Sphere")

if scale_attr := sphere.GetScaleOp().GetAttr():
    scale_attr.Clear()

sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

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

# Export to a new flattened layer for this example.
stage.Export("_assets/timecode_ex2b.usda", addSourceFileComment=False)
```
```{code-cell}
:tags: [remove-input]
DisplayUSD("_assets/timecode_ex2b.usda", show_usd_code=True)
```


## Key Takeaways

To sum it up, time code provides a unitless time ordinate scaled to real-world
time, while time sample stores the actual attribute values at specific time code
ordinates. Understanding these concepts unlocks a way for creating, manipulating, and rendering dynamic scenes and simulations in OpenUSD-based workflows across various industries.

   