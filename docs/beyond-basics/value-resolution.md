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

Value resolution is how OpenUSD figures out the final value of a {term}`property <Property>` or piece of metadata by looking at all the different sources that might have information about it. Think of it like solving a puzzle where you have multiple pieces of information from different places, and you need to figure out what the final answer should be.

Even though value resolution combines many pieces of data together, it's different from composition. Understanding this difference helps you work with USD more effectively.

```{note}
Animation splines were recently added to OpenUSD and are also part of value resolution. We'll update this lesson to include them soon.
```

## How Does It Work?

### Key Differences Between Composition and Value Resolution

1. **{term}`Composition <Composition>` is cached, value resolution is not**

   When you open a {term}`stage <Stage>` or add new scene data, USD creates an {term}`index <Index>` of the composition logic and result at the prim-level for quick access. However, USD doesn't pre-calculate the final values of properties. This keeps the system fast and uses less memory.

   ```{tip}
   If you need to get the same attribute value many times, you can use special tools like `UsdAttributeQuery` to cache this information yourself.
   ```

2. **Composition rules vary by {term}`composition arc <Composition Arcs>`, value resolution rules vary by data type**

   Composition figures out where all the data comes from and creates an index of sources for each prim. Value resolution then takes this ordered list (from strongest to weakest) and combines the opinion data according to what type of information it is.

### Resolving Different Types of Data

#### Resolving Metadata

For most metadata, the rule is simple: **the strongest opinion wins**. Think of it like a voting system where the most authoritative source gets the final say.

Some metadata like prim {term}`specifier <Specifier>`, {term}`attribute <Attribute>` typeName, and several others have special resolution rules. A common metadata type you may encount with special resolution rules are dictionaries (like `customData`). Dictionaries combine element by element, so if one layer has `customData["keyOne"]` and another has `customData["keyTwo"]`, the final result will have both keys.

#### Resolving Relationships

{term}`Relationships <Relationship>` work differently because they can have multiple targets. Instead of just picking the strongest opinion, USD combines all the opinions about what the relationship should point to, following specific rules for how to merge lists (i.e. list ops).

#### Resolving Attributes

Attributes are special because they have three possible sources of values at each location:

1. **{term}`Value Clips <Value Clips>`** - Animation data stored in separate files
2. **{term}`TimeSamples <Time Sample>`** - Specific values at specific times
3. **{term}`Default Value <Default Value>`** - A non-time-varying value

Value resolution of attributes in the first two cases also account for time scaling and offset operators (e.g. {term}`Layer offsets <Layer Offset>`) and {term}`interpolation <Interpolation>` for {term}`time codes <Time Code>` that fall between two explicit timeSamples.

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

This example shows how a transform attribute (the `xformOp:scale` authored by `XformCommonAPI`) resolves from four sources: a {term}`fallback <Fallback>` value when no authored value exists, an authored default value, authored time sample values, and interpolated values between time samples.

```{code-cell}
:emphasize-lines: 27-67
from pxr import Usd, UsdGeom

# Time settings
start_tc = 1
end_tc = 120
cube_anim_start_tc = 60
mid_t = (cube_anim_start_tc + end_tc) // 2
time_code_per_second = 30

# Stage setup
file_path = "_assets/value_resolution_attr.usda"
stage = Usd.Stage.CreateNew(file_path)
stage.SetTimeCodesPerSecond(time_code_per_second)
stage.SetStartTimeCode(start_tc)
stage.SetEndTimeCode(end_tc)

# World, Default Prim, and Ground
world_xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())
UsdGeom.XformCommonAPI(world_xform).SetRotate((-75, 0, 0))

# Create Ground Cube
ground = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("Ground"))
UsdGeom.XformCommonAPI(ground).SetScale((10, 5, 0.1))
UsdGeom.XformCommonAPI(ground).SetTranslate((0, 0, -0.1))

# Static cube with schema-defined default scale (no scale op authored)
static_default_cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("StaticDefaultCube"))
static_default_cube.GetDisplayColorAttr().Set([(0.2, 0.2, 0.8)])
static_default_cube_xform_api = UsdGeom.XformCommonAPI(static_default_cube)
static_default_cube_xform_api.SetTranslate((8, 0, 1))
UsdGeom.Xformable(static_default_cube).AddScaleOp()  # add scale op but do not author a value

# select a non-default cube scale value
cube_set_scale = (1.5, 1.5, 1.5)

# Static cube with an authored default scale (no time samples)
static_cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("StaticCube"))
static_cube.GetDisplayColorAttr().Set([(0.8, 0.2, 0.2)])
static_cube_xform_api = UsdGeom.XformCommonAPI(static_cube)
static_cube_xform_api.SetScale(cube_set_scale)  # set static_cube scale
static_cube_xform_api.SetTranslate((-8, 0, 1.5))

# Animated cube: same default as StaticCube plus time samples
anim_cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendChild("AnimCube"))
anim_cube.GetDisplayColorAttr().Set([(0.2, 0.8, 0.2)])
anim_cube_xform_api = UsdGeom.XformCommonAPI(anim_cube)
anim_cube_xform_api.SetScale(cube_set_scale)  # SAME as static_cube
anim_cube_xform_api.SetTranslate((0, 0, 1.5))

# Author time samples for scale and translate
# anim_cube_xform_api.SetScale(cube_set_scale, Usd.TimeCode(start_tc))
anim_cube_xform_api.SetScale((2.5, 2.5, 2.5), Usd.TimeCode(cube_anim_start_tc))  # first animated sample
anim_cube_xform_api.SetScale((5, 5, 5), Usd.TimeCode(end_tc))  # last sample
anim_cube_xform_api.SetTranslate((0, 0, 2.5), Usd.TimeCode(cube_anim_start_tc))
anim_cube_xform_api.SetTranslate((0, 0, 5.0), Usd.TimeCode(end_tc))

# Read back using resolved scale values
_, _, default_cube_fallback_scale, _, _ = UsdGeom.XformCommonAPI(static_default_cube).GetXformVectors(Usd.TimeCode.Default())
_, _, static_cube_default_scale, _, _ = static_cube_xform_api.GetXformVectors(Usd.TimeCode.Default())
_, _, anim_cube_default_scale, _, _ = anim_cube_xform_api.GetXformVectors(Usd.TimeCode.Default())
_, _, anim_cube_earliest_scale, _, _ = anim_cube_xform_api.GetXformVectors(Usd.TimeCode.EarliestTime())
_, _, anim_cube_tc1_scale, _, _ = anim_cube_xform_api.GetXformVectors(Usd.TimeCode(start_tc))
_, _, scale_mid, _, _ = anim_cube_xform_api.GetXformVectors(Usd.TimeCode(mid_t))

# Illustrate that Get() is the same as Get(Usd.TimeCode.Default())
no_time_code_is_default = static_cube.GetSizeAttr().Get() == static_cube.GetSizeAttr().Get(Usd.TimeCode.Default())

print(f"When querying a value Get() is the same as Get(Usd.TimeCode.Default()): {no_time_code_is_default}\n")

print(f"Scale - StaticDefaultCube (no authored xformOp:scale -> schema fallback):  {default_cube_fallback_scale}")  # returns identity fallback value.
print(f"Scale - StaticCube (authored default at Default time):  {static_cube_default_scale}")  # returns the user authored default value.
print(f"Scale - AnimCube (authored default at Default time):  {anim_cube_default_scale}")  # returns the user authored default value.
print(f"Scale - AnimCube at EarliestTime t={cube_anim_start_tc}:  {anim_cube_earliest_scale}")  # first authored time sample value
print(f"Scale - AnimCube at t={start_tc} (before first sample, clamped):  {anim_cube_tc1_scale}")  # resolved value prior to authored value.
print(f"Scale - AnimCube at mid_t={mid_t} (interpolated):  {scale_mid}")  # interpolated between samples

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```
Notice `Get(..., Usd.TimeCode.Default())` returns the user defined default (non‑time‑sampled) value, `Get(..., Usd.TimeCode.EarliestTime())` returns the first time sampled value, and if a **time before the first sample is queried USD also returns the first sampled value**.

### Example 2: Custom Data and Relationship Value Resolution

This example composes {term}`layers <Layer>` to show two resolution rules for dictionary metadata like `customData` (per key by strength) as well as relationships `list‑editing semantics`.

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
Here `source` and `opinion` resolve from the stronger layer, while `unique_layer_value` persists from the weaker layer since the stronger layer did not author that key. The resolved relationship includes both `LookA` and `LookB` because {term}`list‑editing <List Editing>` merged the targets.

## Key Takeaways

Value resolution gives OpenUSD its powerful ability to combine data from multiple sources while keeping the system fast and efficient.

This is incredibly useful in real-world workflows. For example, imagine multiple teams working on different parts of a scene - value resolution seamlessly combines everyone's work into a single model without anyone's contributions being lost.

Here's a concrete example with a robot arm:

* The base layer defines the robot arm's default position at `(0, 0, 0)`
* The animation layer overrides this to move the arm to `(5, 0, 0)` during operation

During value resolution, OpenUSD combines these layers, resulting in the robot arm being positioned at `(5, 0, 0)` while keeping all other unchanged properties from the base layer.

Understanding value resolution is key to working effectively with OpenUSD's non-destructive workflow and getting the best performance in multi-threaded applications.
