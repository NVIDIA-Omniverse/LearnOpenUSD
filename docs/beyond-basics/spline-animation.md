---
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

# Spline Animation

## What Is Spline Animation?

{term}`Time samples <Time Sample>` are a straightforward way to animate {term}`attributes <Attribute>`: you author values at chosen {term}`time codes <Time Code>`, and USD interpolates between them (for example, linearly). That model is a good fit when motion is simple or nearly piecewise linear.

An {term}`animation spline <Animation Spline>` stores a curve defined by **knots** (time-value keys), tangent data, and interpolation modes between knots. Splines can represent smoother or sparser animation than dense time-sample sequences, and they support **inner loops** (repeating a prototype segment with a value offset) and **extrapolation** past the authored knot range (for example, repeating the whole curve). Pipeline tools and DCC exports can author splines directly on attributes that support them.

## How Does It Work?

This lesson shows how to build splines with the Python `pxr.Ts` helpers, attach them to a transform operation with `UsdAttribute.SetSpline`, and see how {term}`layer offsets <Layer Offset>` apply to spline-evaluated motion the same way they do for time samples. For the full rules engine that merges defaults, time samples, splines, and more, see {term}`value resolution <Value Resolution>`.

```{note}
Stage timing metadata (`timeCodesPerSecond`, `startTimeCode`, `endTimeCode`) still defines how time codes map to seconds for playback. When layers disagree on frame rate, USD reconciles timing during value resolution; see [Units in OpenUSD](units.md) for `timeCodesPerSecond` behavior.
```

```{tip}
The embedded **3D previews** in this site use GLB conversion that keys off **time samples**, not raw spline payloads. Each example calls `DisplayUSD(..., bake_splines_for_display=True)`, which writes a temporary flattened USD and **evaluates splines into dense samples** for the viewer only. Your saved `_assets/*.usda` files stay spline-authored; open them in **usdview** to inspect splines directly.
```

## Working With Python

The `Ts` package provides `Ts.Spline`, `Ts.Knot`, `Ts.LoopParams`, and `Ts.Extrapolation`. You construct a spline for an attribute’s value type (for example `"float"`), add knots, optionally configure loop or extrapolation settings, then call `UsdAttribute.SetSpline`.

```{attention}
Splines are only supported on **floating-point scalar** attributes: `half`, `float`, and `double`. `Ts.Spline` raises an error for any other type name, so the multi-axis transform ops cannot be splined directly: `AddTranslateOp`, `AddRotateXYZOp`, and `AddScaleOp` all produce a 3-component type (`float3`, `double3`, or `half3`, depending on the precision you request).

Use the single-axis ops instead, or author one spline per component. Single-axis ops are always scalar—`AddRotateZOp` yields a `float` by default and `AddTranslateXOp` a `double`, and passing `UsdGeom.XformOp.PrecisionHalf` or `PrecisionDouble` still gives you `half` or `double`. That is why the examples below can pass `attr.GetTypeName()` straight to `Ts.Spline`: every precision those ops can produce is one splines support.
```

Reading `attr.Get(timeCode)` evaluates the composed spline at that time, subject to layer time mapping—**provided no time samples are authored for that attribute at a stronger or equal location**. Time samples win over splines during {term}`value resolution <Value Resolution>`, so an attribute carrying both returns the sampled value and `attr.HasSpline()` reports `False`.

The snippet below is a complete, self-contained example:

```python
from pxr import Usd, UsdGeom, Ts

stage = Usd.Stage.CreateInMemory()
xform = UsdGeom.Xform.Define(stage, "/World/Spinner")

# xformOp:rotateZ is a float attribute, which splines support
spin = xform.AddRotateZOp(opSuffix="yaw")
attr = spin.GetAttr()
type_name = str(attr.GetTypeName())
spline = Ts.Spline(type_name)
spline.SetKnot(
    Ts.Knot(
        typeName=type_name,
        time=0,
        value=0,
        nextInterp=Ts.InterpLinear,
    )
)
spline.SetKnot(
    Ts.Knot(
        typeName=type_name,
        time=48,
        value=180,
        nextInterp=Ts.InterpLinear,
    )
)
attr.SetSpline(spline)
```

For extrapolation modes, knot tangents, and multi-dimensional types, see the OpenUSD C++ documentation for [`TsSpline`](https://openusd.org/release/api/class_ts_spline.html).

## Examples

```{tip}
You can run these examples locally as Jupyter notebooks. See [How to Run Notebooks Locally](../jupyter-notebook-setup.md) for setup instructions.
```

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
:test-tags: [spline-animation-setup]
from lousd.utils.visualization import DisplayUSD
from lousd.utils.helperfunctions import create_new_stage
```

### Example 1: Inner loop on a rotation

Here a single linear segment from 0° to 90° over 24 frames is repeated four times (one prototype plus three post-loops) with a **value offset** of 90° each time, so the cube completes a full 360° turn without authoring every quarter-turn as separate samples.

```{code-cell}
:test-tags: [spline-animation-inner-loop]
:emphasize-lines: 22-38
from pxr import Usd, UsdGeom, Ts

spline_loop_path = "_assets/spline_inner_loop.usda"
stage = create_new_stage(spline_loop_path)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(96)

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

xform = UsdGeom.Xform.Define(stage, "/World/RotatingCube")
cube = UsdGeom.Cube.Define(stage, "/World/RotatingCube/Geometry")
cube.GetSizeAttr().Set(1.2)
cube.GetDisplayColorAttr().Set([(0.35, 0.65, 0.95)])

yaw = xform.AddRotateZOp(opSuffix="yaw")
yaw_attr = yaw.GetAttr()
type_name = str(yaw_attr.GetTypeName())

spline = Ts.Spline(type_name)
spline.SetKnot(
    Ts.Knot(
        typeName=type_name,
        time=0,
        value=0,
        nextInterp=Ts.InterpLinear,
    )
)
loop_params = Ts.LoopParams()
loop_params.protoStart = 0
loop_params.protoEnd = 24
loop_params.numPostLoops = 3
loop_params.valueOffset = 90
spline.SetInnerLoopParams(loop_params)
yaw_attr.SetSpline(spline)

stage.Save()

mid_proto = 12
print(f"Rotation at t=0: {yaw_attr.Get(0)}")
print(f"Rotation at t={mid_proto} (mid prototype): {yaw_attr.Get(mid_proto)}")
print(f"Rotation at t=24 (end of first loop): {yaw_attr.Get(24)}")
print(f"Rotation at t=48: {yaw_attr.Get(48)}")
print(f"Attribute stores a spline: {yaw_attr.HasSpline()}")
```

```{code-cell}
:tags: [remove-input]
DisplayUSD(spline_loop_path, show_usd_code=True, bake_splines_for_display=True)
```

The `.spline` payload in USD text lists the loop parameters and knot data. At evaluation time, value resolution samples that curve at the requested time code.

### Example 2: Post extrapolation

Without extrapolation, querying times past the last knot **holds** the last value. Setting **post extrapolation** lets motion continue for the rest of the stage range (or until another rule applies).

This example rocks a cube on the Y axis from -12° to 12° over 60 frames, then keeps swinging by mirroring that segment with `Ts.ExtrapLoopOscillate`.

```{code-cell}
:test-tags: [spline-animation-extrapolation]
:emphasize-lines: 18-26
from pxr import Usd, UsdGeom, Ts

spline_extrap_path = "_assets/spline_extrapolation.usda"
stage = create_new_stage(spline_extrap_path)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(30)
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(150)

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

xform = UsdGeom.Xform.Define(stage, "/World/RockingCube")
cube = UsdGeom.Cube.Define(stage, "/World/RockingCube/Geometry")
cube.GetSizeAttr().Set(1.0)
cube.GetDisplayColorAttr().Set([(0.9, 0.55, 0.25)])

rock = xform.AddRotateYOp(opSuffix="rock")
rock_attr = rock.GetAttr()
type_name = str(rock_attr.GetTypeName())

spline = Ts.Spline(type_name)
spline.SetKnot(
    Ts.Knot(
        typeName=type_name,
        time=0,
        value=-12,
        nextInterp=Ts.InterpCurve,
    )
)
spline.SetKnot(
    Ts.Knot(
        typeName=type_name,
        time=60,
        value=12,
        nextInterp=Ts.InterpCurve,
    )
)
spline.SetPostExtrapolation(Ts.Extrapolation(Ts.ExtrapLoopOscillate))
rock_attr.SetSpline(spline)

stage.Save()

print(f"t=45 (within authored span): {rock_attr.Get(45):.2f}")
print(f"t=75 (past the last knot, swinging back): {rock_attr.Get(75):.2f}")
print(f"t=120 (one full oscillation later): {rock_attr.Get(120):.2f}")
```

```{code-cell}
:tags: [remove-input]
DisplayUSD(spline_extrap_path, show_usd_code=True, bake_splines_for_display=True)
```

`Ts.ExtrapLoopOscillate` continues the spline by mirroring the authored segment, so the cube swings back to -12° and repeats. Choose the mode that matches the motion: `Ts.ExtrapLoopRepeat` repeats the segment's *shape* and offsets each cycle by the difference between the first and last knot values, which would keep turning this cube in one direction instead of rocking it.

### Example 3: Layer offsets and spline time

{term}`References <Reference>` can carry an `Sdf.LayerOffset` (scale and offset on the **source** layer’s time line). The same rules apply when the referenced animation is driven by splines: evaluation uses the mapped time when resolving values on the composed stage.

```{code-cell}
:test-tags: [spline-animation-layer-offset]
:emphasize-lines: 28-42
from pxr import Usd, UsdGeom, Ts, Sdf

slide_asset_path = "_assets/spline_slide_rig.usda"
rig_stage = create_new_stage(slide_asset_path)
UsdGeom.SetStageUpAxis(rig_stage, UsdGeom.Tokens.y)
rig_stage.SetTimeCodesPerSecond(24)
rig_stage.SetStartTimeCode(0)
rig_stage.SetEndTimeCode(48)

rig = UsdGeom.Xform.Define(rig_stage, "/SlideRig")
rig_stage.SetDefaultPrim(rig.GetPrim())
UsdGeom.Cube.Define(rig_stage, "/SlideRig/Geometry").GetSizeAttr().Set(0.6)

slide = rig.AddTranslateXOp(opSuffix="slide")
slide_attr = slide.GetAttr()
type_name = str(slide_attr.GetTypeName())

spline = Ts.Spline(type_name)
spline.SetKnot(
    Ts.Knot(typeName=type_name, time=0, value=0, nextInterp=Ts.InterpLinear)
)
spline.SetKnot(
    Ts.Knot(typeName=type_name, time=48, value=4, nextInterp=Ts.InterpLinear)
)
slide_attr.SetSpline(spline)
rig_stage.Save()

offset_scene_path = "_assets/spline_layer_offset_scene.usda"
scene = create_new_stage(offset_scene_path)
UsdGeom.SetStageUpAxis(scene, UsdGeom.Tokens.y)
scene.SetTimeCodesPerSecond(24)
scene.SetStartTimeCode(0)
scene.SetEndTimeCode(48)

UsdGeom.Xform.Define(scene, "/World")
scene.SetDefaultPrim(scene.GetPrimAtPath("/World"))

left_rig = UsdGeom.Xform.Define(scene, "/World/LeftRig")
left_rig.GetPrim().GetReferences().AddReference(slide_asset_path, primPath="/SlideRig")

right_rig = UsdGeom.Xform.Define(scene, "/World/RightRig")
right_rig.GetPrim().GetReferences().AddReference(
    slide_asset_path,
    primPath="/SlideRig",
    layerOffset=Sdf.LayerOffset(offset=24),
)

scene.Save()

composed = Usd.Stage.Open(offset_scene_path)
early = composed.GetPrimAtPath("/World/LeftRig").GetAttribute("xformOp:translateX:slide")
late = composed.GetPrimAtPath("/World/RightRig").GetAttribute("xformOp:translateX:slide")
t_query = 24
print(f"At global t={t_query}, left rig X (no offset): {early.Get(t_query)}")
print(f"At global t={t_query}, right rig X (offset +24): {late.Get(t_query)}")
```

```{code-cell}
:tags: [remove-input]
DisplayUSD(offset_scene_path, show_usd_code=True, bake_splines_for_display=True)
```

The right instance sees source time `t - 24` at global time `t`, so at global frame 24 it is only at the start of its slide. For deeper retiming, {term}`value clips <Value Clips>` remain the heavier-weight option.

## Key Takeaways

1. **Splines complement time samples** on the same attributes: you can author smooth, looping, or extrapolated motion without dense sample lists, where tooling supports spline authoring.
2. **`pxr.Ts` + `SetSpline`** is the usual Python path for constructing curves, inner loops, and extrapolation before saving USD.
3. **Splines are for `half`, `float`, and `double` attributes only**—animate single-axis transform ops, or one spline per component, rather than vector types like `double3`.
4. **Resolution is per time code**: `Get(t)` evaluates the composed spline (after strength ordering and time mapping), consistent with how samples and `timeCodesPerSecond` interact across layers. Time samples at a stronger or equal location take precedence over a spline.
5. **Layer offsets retime splines** just like samples—plan for held behavior outside knot coverage if you rely on offsets or short authored ranges.

For how defaults, samples, splines, and clips combine in the attribute stack, see [Value resolution](value-resolution.md).
