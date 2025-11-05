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

# Value Resolution

## What Is Value Resolution?

![Value Resolution Definition](../images/foundations/ValueResolution_Defintion.webm)

Value resolution is how OpenUSD figures out the final value of a property or piece of metadata by looking at all the different sources that might have information about it. Think of it like solving a puzzle where you have multiple pieces of information from different places, and you need to figure out what the final answer should be.

Even though value resolution combines many pieces of data together, it's different from composition. Understanding this difference helps you work with USD more effectively.

```{note}
Animation splines were recently added to OpenUSD and are also part of value resolution. We'll update this lesson to include them soon.
```

## How Does It Work?

### Key Differences Between Composition and Value Resolution

1. **Composition is cached, value resolution is not**

   When you open a stage or add new scene data, USD creates an "index" of the composition logic and result at the prim-level for quick access. However, USD doesn't pre-calculate the final values of properties. This keeps the system fast and uses less memory.

   ```{tip}
   If you need to get the same attribute value many times, you can use special tools like `UsdAttributeQuery` to cache this information yourself.
   ```

2. **Composition rules vary by composition arc, value resolution rules vary by data type**

   Composition figures out where all the data comes from and creates an index of sources for each prim. Value resolution then takes this ordered list (from strongest to weakest) and combines the opinion data according to what type of information it is.

### Resolving Different Types of Data

#### Resolving Metadata

For most metadata, the rule is simple: **the strongest opinion wins**. Think of it like a voting system where the most authoritative source gets the final say.

Some metadata like prim specifier, attribute typeName, and several others have special resolution 
rules. A common metadata type you may encount with special resolution rules are dictionaries (like `customData`). Dictionaries combine element by element, so if one layer has `customData["keyOne"]` and another has `customData["keyTwo"]`, the final result will have both keys.

#### Resolving Relationships

Relationships work differently because they can have multiple targets. Instead of just picking the strongest opinion, USD combines all the opinions about what the relationship should point to, following specific rules for how to merge lists (i.e. list ops).

#### Resolving Attributes

Attributes are special because they have three possible sources of values at each location:

1. **Value Clips** - Animation data stored in separate files
2. **TimeSamples** - Specific values at specific times
3. **Default Value** - A non-time-varying value

Value resolution of attributes in the first two cases also account for time scaling and offset operators (e.g. Layer Offsets) and interpolation for time codes that fall between two explicit timeSamples.

## Working With Python

```python
from pxr import Usd, UsdGeom

# Open a stage
stage = Usd.Stage.Open('example.usd')

# Get a prim
prim = stage.GetPrimAtPath('/World/MyPrim')

# Get an attribute
attr = prim.GetAttribute('myAttribute')
# Usd.TimeCode.Default() is implied
default_value = attr.Get()
# Get the value at time code 100.
animated_value = attr.Get(100)
# Use EarliestTime to get earliest animated values if they exist
value = attr.Get(Usd.TimeCode.EarliestTime())
```

When you get an attribute value without an explicit time code, the default time code (`UsdTimeCode::Default()`) is usually not what you want if your stage has animation. Instead, use `UsdTimeCode::EarliestTime()` to make sure you get the actual animated values rather than just the default value.

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
from utils.helperfunctions import create_new_stage
```

### Example 1: Attribute Value Resolution and Animation

This example demonstrates how attribute (scale) values are resolved across schema defined defaults, user defined defaults, and user defined time sampled values.

```{code-cell}
:emphasize-lines: 27-60
from pxr import Usd, UsdGeom

# Time settings
start_tc = 1
end_tc = 120
cube_anim_start_tc = 60
time_code_per_second = 30

# Stage and interpolation
file_path = "_assets/value_resolution_attr.usda"
stage = Usd.Stage.CreateNew(file_path)
stage.SetTimeCodesPerSecond(time_code_per_second)
stage.SetStartTimeCode(start_tc)
stage.SetEndTimeCode(end_tc)

# World and a simple world rotation over time (children inherit transforms)
world_xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())
UsdGeom.XformCommonAPI(world_xform).SetRotate((-75, 0, 0))

# Create Ground cube
background = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("Ground"))
UsdGeom.XformCommonAPI(background).SetScale((10, 5, 0.1))
UsdGeom.XformCommonAPI(background).SetTranslate((0, 0, -0.1))


# Static cube with default (schema defined) scale
static_default_cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("StaticDefaultCube"))
static_default_cube.GetDisplayColorAttr().Set([(0.2, 0.2, 0.8)])
UsdGeom.XformCommonAPI(static_default_cube).SetTranslate((8, 0, 1))

# select a non-default cube scale value
cube_set_scale = (1.5, 1.5, 1.5)

# Static cube with cube_set_scale scale set
static_cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("StaticCube"))
static_cube.GetDisplayColorAttr().Set([(0.8, 0.2, 0.2)])
static_cube_xform_api = UsdGeom.XformCommonAPI(static_cube)
static_cube_xform_api.SetScale(cube_set_scale)  # set static_cube scale
static_cube_xform_api.SetTranslate((-8, 0, 1.5))

# Animated cube with cube_set_scale set
anim_cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("AnimCube"))
anim_cube.GetDisplayColorAttr().Set([(0.2, 0.8, 0.2)])
anim_cube_xform_api = UsdGeom.XformCommonAPI(anim_cube)
anim_cube_xform_api.SetScale(cube_set_scale)  # SAME as static_cube
anim_cube_xform_api.SetTranslate((0, 0, 1.5))

# Set scale with specified Usd.TimeCode values
# anim_cube_xform_api.SetScale(cube_set_scale, Usd.TimeCode(start_tc))
anim_cube_xform_api.SetScale((2.5, 2.5, 2.5), Usd.TimeCode(cube_anim_start_tc))  # first animated sample
anim_cube_xform_api.SetScale((5, 5, 5), Usd.TimeCode(end_tc))  # last sample
anim_cube_xform_api.SetTranslate((0, 0, 2.5), Usd.TimeCode(cube_anim_start_tc))
anim_cube_xform_api.SetTranslate((0, 0, 5.0), Usd.TimeCode(end_tc))

# Print resolved values
_, _, anim_cube_default_scale, _, _ = anim_cube_xform_api.GetXformVectors(Usd.TimeCode.Default())
_, _, anim_cube_earliest_scale, _, _ = anim_cube_xform_api.GetXformVectors(Usd.TimeCode.EarliestTime())
print("Default Scale on anim_cube:", anim_cube_default_scale)  # returns the user defined default value.
print(f"Scale for anim_cube at EarliestTime t={cube_anim_start_tc}:", anim_cube_earliest_scale)  # first authored sample

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path)
```
Notice that values are resolved differently when `Usd.TimeCode` is used, including at times before the first authored `Usd.TimeCode`.

### Example 2: Custom Data and Relationship Value Resolution

This example demonstrates how custom data and relationship values are resolved across multiple layers. Custom data dictionaries are resolved per key and based on layer order. Relationships are list edited and not dependent on layer order.

```{code-cell}
:emphasize-lines: 37-60
from pxr import Usd, UsdGeom
import os

# --- Layer 1 (weaker)
layer_1_path = "_assets/value_resolution_layer_1.usda"
layer_1_stage = Usd.Stage.CreateNew(layer_1_path)

layer_1_xform = UsdGeom.Xform.Define(layer_1_stage, "/World/XformPrim")
layer_1_xform_prim = layer_1_xform.GetPrim()

# "/World/XformPrim" customData
layer_1_xform_prim.SetCustomDataByKey("source",  "layer_1")
layer_1_xform_prim.SetCustomDataByKey("opinion",  "weak")
layer_1_xform_prim.SetCustomDataByKey("unique_layer_value", "layer_1_unique_value")  # only authored in layer_1

# Relationship contribution from base
look_a = UsdGeom.Xform.Define(layer_1_stage, "/World/Looks/LookA")
layer_1_xform_prim.CreateRelationship("look:targets").AddTarget(look_a.GetPath())
layer_1_stage.Save()

# --- Layer 2 (stronger)
layer_2_path = "_assets/value_resolution_layer_2.usda"
layer_2_stage = Usd.Stage.CreateNew(layer_2_path)

layer_2_xform = UsdGeom.Xform.Define(layer_2_stage, "/World/XformPrim")
layer_2_xform_prim = layer_2_xform.GetPrim()

# "/World/XformPrim" customData
layer_2_xform_prim.SetCustomDataByKey("source",  "layer_2")
layer_2_xform_prim.SetCustomDataByKey("opinion",  "strong")

# Relationship contribution from override
look_b = UsdGeom.Xform.Define(layer_2_stage, "/World/Looks/LookB")
layer_2_xform_prim.CreateRelationship("look:targets").AddTarget(look_b.GetPath())
layer_2_stage.Save()

# --- Composed stage. First sublayer listed (layer_2) is strongest
composed_path = "_assets/value_resolution_composed.usda"
composed_stage = Usd.Stage.CreateNew(composed_path)
composed_stage.GetRootLayer().subLayerPaths = [os.path.basename(layer_2_path), os.path.basename(layer_1_path)]

xform_prim = composed_stage.GetPrimAtPath("/World/XformPrim")
resolved_custom_data = xform_prim.GetCustomData() 

# resolved custom data:
print("Resolved CustomData:")
for key, value in resolved_custom_data.items():
    print(f"- '{key}': '{value}'")

# resolved relationship targets:
targets = xform_prim.GetRelationship("look:targets").GetTargets()
print(f"\nResolved relationship targets: {[str(t) for t in targets]}")  # both LookA and LookB

composed_stage.Save()

# Write out the composed stage to a single file for inspection
explicit_composed_path = '_assets/value_resolution_composed_explicit.usda'
txt = composed_stage.ExportToString(addSourceFileComment=False)
with open(explicit_composed_path, "w") as f:
    f.write(txt)
```
```{code-cell}
:tags: [remove-input]
DisplayCode(explicit_composed_path)
```

## Key Takeaways

Value resolution gives OpenUSD its powerful ability to combine data from multiple sources while keeping the system fast and efficient.

This is incredibly useful in real-world workflows. For example, imagine multiple teams working on different parts of a scene - value resolution seamlessly combines everyone's work into a single model without anyone's contributions being lost.

Here's a concrete example with a robot arm:

* The base layer defines the robot arm's default position at `(0, 0, 0)`
* The animation layer overrides this to move the arm to `(5, 0, 0)` during operation

During value resolution, OpenUSD combines these layers, resulting in the robot arm being positioned at `(5, 0, 0)` while keeping all other unchanged properties from the base layer.

Understanding value resolution is key to working effectively with OpenUSD's non-destructive workflow and getting the best performance in multi-threaded applications.
