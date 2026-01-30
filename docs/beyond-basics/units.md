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

# Units in OpenUSD

## What Are Units?

When assembling 3D content from various sources—whether created in Blender at meter scale, Houdini in centimeters, or Revit in feet—ensuring consistent interpretation of units is critical for coherent scene {term}`composition <Composition>`. USD provides several {term}`stage <Stage>` {term}`metadata <Metadata>` fields to encode unit information:

- **`metersPerUnit`** (MPU) - Defines the linear scale of geometry in the file relative to meters. For example, `0.01` means content is encoded in centimeters (0.01 meters per unit), while `1.0` means content is in meters.
- **`upAxis`** - Specifies the coordinate system orientation, typically `"Y"` or `"Z"`.
- **`kilogramsPerUnit`** (KGPU) - Defines the mass/density scale for physics simulations, representing kilograms per unit cubed.
- **`timeCodesPerSecond`** - Defines the temporal scale for animation, mapping {term}`time codes <Time Code>` to real-world seconds.

These metadata fields help USD understand the intent of content creators and enable correct interpretation when multiple {term}`layers <Layer>` are composed together.

```{note}
If `metersPerUnit` is not explicitly authored in a USD file, the fallback value is `0.01` (centimeters). For `upAxis`, the fallback is `"Y"`.
```

### Why Units Matter

Consider a pipeline where:
- An environment {term}`asset <Asset>` is built in meters (`metersPerUnit = 1.0`)
- A character asset is built in centimeters (`metersPerUnit = 0.01`)
- Both assets are {term}`referenced <Reference>` into the same scene

Without proper unit handling, a 2-meter tall character would appear as 2 centimeters tall when composed into a meter-based scene—100 times too small. Understanding how USD handles unit metadata during composition is essential for building robust pipelines.

## How Does It Work?

### Automatic vs. Manual Unit Reconciliation

A critical aspect of USD's unit system is that **not all unit metadata is handled the same way during composition**. This distinction is important for pipeline developers to understand:

#### Automatically Handled 

* `timeCodesPerSecond`

When layers with different `timeCodesPerSecond` values are composed (via {term}`sublayers <Sublayer>`, {term}`references <Reference>`, or {term}`payloads <Payload>`), USD **automatically scales {term}`time samples <Time Sample>`** so animations play back correctly relative to the root layer's `timeCodesPerSecond`.

For example, if your root layer has `timeCodesPerSecond = 24` and you reference a layer with `timeCodesPerSecond = 60`, USD automatically adjusts the time samples from the referenced layer so the animation timing remains correct. This automatic scaling happens transparently during {term}`value resolution <Value Resolution>`.

#### Manually Handled

* `upAxis`
* `metersPerUnit`
* `kilogramsPerUnit`

In contrast, **USD does not automatically reconcile** geometric and physics unit metadata. According to the {usdcpp}`OpenUSD documentation <UsdGeomLinearUnits_group Details>`:

 

> "As with encoding stage `upAxis`, we restrict the encoding of linear units to be stage-wide; **if assembling assets of different metrics, it is the assembler's responsibility to apply suitable correctives** to the referenced data to bring it into the referencing stage's metric."

This means:
- A 6-meter tall tree (`metersPerUnit = 1.0`) referenced into a centimeter-based stage (`metersPerUnit = 0.01`) will compose as 6 centimeters tall by default—100 times too small
- Different `upAxis` values across composed layers require manual coordinate transformations
- The pipeline must apply scale corrections or ensure unit consistency upstream

### Common metersPerUnit Values

Here are typical MPU values for common units:

| Unit | metersPerUnit |
|------|---------------|
| Kilometers | 1000 |
| Meters | 1.0 |
| Centimeters | 0.01 |
| Millimeters | 0.001 |
| Inches | 0.0254 |
| Feet | 0.3048 |
| Miles | 1609.34 |

### Pipeline Strategies

Production pipelines typically handle unit mismatches through one of these approaches:

1. **Organization-wide standards**: Establish conventions (e.g., "all assets use centimeters and Z-up") and enforce them during asset creation
2. **Explicit scale correction**: Apply corrective transforms when referencing assets with different units
3. **Conversion tools**: Build importers/exporters that normalize units during asset ingestion
4. **Metadata validation**: Use {term}`asset validation <Asset Info>` tools to flag unit mismatches before composition

## Working With Python

USD provides APIs for querying and setting stage unit metadata:

```python
from pxr import Usd, UsdGeom, UsdPhysics

# Create or open a stage
stage = Usd.Stage.CreateNew("example.usda")

# Get and set metersPerUnit
current_mpu = UsdGeom.GetStageMetersPerUnit(stage)
print(f"Current metersPerUnit: {current_mpu}")

UsdGeom.SetStageMetersPerUnit(stage, 0.0254)  # Set to inches
print(f"Updated to: {UsdGeom.GetStageMetersPerUnit(stage)}")

# Get and set upAxis
current_up = UsdGeom.GetStageUpAxis(stage)
print(f"Current upAxis: {current_up}")

UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)  # Set to Z-up
print(f"Updated to: {UsdGeom.GetStageUpAxis(stage)}")

# Get and set timeCodesPerSecond (stage method, not UsdGeom)
current_tcps = stage.GetTimeCodesPerSecond()
print(f"Current timeCodesPerSecond: {current_tcps}")

stage.SetTimeCodesPerSecond(48)
print(f"Updated to: {stage.GetTimeCodesPerSecond()}")

# Get and set kilogramsPerUnit using UsdPhysics schema
current_kgpu = UsdPhysics.GetStageKilogramsPerUnit(stage)
print(f"Current kilogramsPerUnit: {current_kgpu}")

UsdPhysics.SetStageKilogramsPerUnit(stage, 0.001)  # Set to grams
print(f"Updated to: {UsdPhysics.GetStageKilogramsPerUnit(stage)}")
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from lousd.utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Demonstrating metersPerUnit Composition Behavior

This example shows what happens when assets with different `metersPerUnit` values are composed together without manual correction. We'll create two cube assets that both represent 1-meter cubes, but authored at different unit scales:

1. A 1-meter cube authored in **centimeters** (`metersPerUnit = 0.01`), with `size = 100.0`
2. A 1-meter cube authored in **millimeters** (`metersPerUnit = 0.001`), with `size = 1000.0`

Both cubes represent the same real-world size—1 meter. If USD automatically converted units during composition, both cubes would appear identical when referenced into any scene regardless of that scene's `metersPerUnit`. Let's see what actually happens when we reference both into a millimeter-scale scene.

```{code-cell}
:emphasize-lines: 7,10-11,25,28-29,50-51,54-55
from pxr import Usd, UsdGeom, Sdf, Gf

# Create a cube asset in CENTIMETERS (metersPerUnit = 0.01)
cm_asset_path = "_assets/1m_cube_centimeters.usda"
cm_stage = Usd.Stage.CreateNew(cm_asset_path)
UsdGeom.SetStageUpAxis(cm_stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(cm_stage, 0.01)  # Centimeters

# Create a 1 meter cube in centimeter coordinate system
cube_in_cm = UsdGeom.Cube.Define(cm_stage, "/Cube")
cube_in_cm.GetSizeAttr().Set(100.0)
cube_in_cm.GetDisplayColorAttr().Set([(0.2, 0.6, 0.9)])

# Position and save
cm_stage.SetDefaultPrim(cube_in_cm.GetPrim())
cm_stage.Save()

print(f"Centimeter asset: size = { cube_in_cm.GetSizeAttr().Get()} at metersPerUnit = {UsdGeom.GetStageMetersPerUnit(cm_stage)}")
print(f"  -> Represents a {cube_in_cm.GetSizeAttr().Get() * UsdGeom.GetStageMetersPerUnit(cm_stage):.1f} meter cube\n")

# Create a cube asset in MILLIMETERS (metersPerUnit = 0.001)
mm_asset_path = "_assets/cube_in_millimeters.usda"
mm_stage = Usd.Stage.CreateNew(mm_asset_path)
UsdGeom.SetStageUpAxis(mm_stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(mm_stage, 0.001)  # Millimeters

# Create a 1 meter cube in millimeter coordinate system
cube_in_mm = UsdGeom.Cube.Define(mm_stage, "/Cube")
cube_in_mm.GetSizeAttr().Set(1000.0)
cube_in_mm.GetDisplayColorAttr().Set([(0.9, 0.5, 0.2)])

# Position and save
mm_stage.SetDefaultPrim(cube_in_mm.GetPrim())
mm_stage.Save()

print(f"Millimeter asset: size = { cube_in_mm.GetSizeAttr().Get()} at metersPerUnit = {UsdGeom.GetStageMetersPerUnit(mm_stage)}")
print(f"  -> Represents a {cube_in_mm.GetSizeAttr().Get() * UsdGeom.GetStageMetersPerUnit(mm_stage):.1f} meter cube\n")

# Create a scene that references both cubes (using millimeter scale)
scene_path = "_assets/units_mismatch_scene.usda"
scene_stage = Usd.Stage.CreateNew(scene_path)
UsdGeom.SetStageUpAxis(scene_stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(scene_stage, 0.001)  # Scene is in millimeters

# Add both cube references
world = UsdGeom.Xform.Define(scene_stage, "/World")
scene_stage.SetDefaultPrim(world.GetPrim())

meter_ref = scene_stage.DefinePrim("/World/Cube_1m_In_Centimeters")
meter_ref.GetReferences().AddReference(cm_asset_path)
UsdGeom.XformCommonAPI(meter_ref).SetTranslate(Gf.Vec3d(-1000, 0, 0))

cm_ref = scene_stage.DefinePrim("/World/Cube_1m_In_Millimeters")
cm_ref.GetReferences().AddReference(mm_asset_path)
UsdGeom.XformCommonAPI(cm_ref).SetTranslate(Gf.Vec3d(1000, 0, 0)) 

scene_stage.Save()

print("Scene composition (metersPerUnit = 0.01):")
print("  - Referenced 1m cube in centimeter-scale appears 10x too small")
print("  - Referenced 1m cube in millimeter-scale appear correctly")
```

```{code-cell}
:tags: [remove-input]
DisplayUSD(scene_path, show_usd_code=True)
```

Notice the size discrepancy: even though both cubes represent 1 meter in their respective source files, they appear at different sizes in the composed scene. Here's what happened:

**The centimeter cube (blue)** was authored with `size = 100.0` at `metersPerUnit = 0.01`. When referenced into the millimeter scene (`metersPerUnit = 0.001`), USD does not perform any unit conversion—it simply brings in the raw value of `100.0` units. In the millimeter coordinate system, 100 units equals 0.1 meters (100 × 0.001), making it appear **10 times too small**.

**The millimeter cube (orange)** was authored with `size = 1000.0` at `metersPerUnit = 0.001`. Since the scene also uses millimeters, the value of 1000 units equals 1 meter (1000 × 0.001), so it appears at the **correct size**.

This demonstrates USD's fundamental behavior: **geometric values are copied literally without unit conversion**. To properly handle the centimeter cube in this millimeter scene, the pipeline would need to apply a 10× scale transform to compensate for the unit mismatch.

Flattening the stage reveals exactly what USD composed—the raw attribute values without any unit-based scaling:
```{code-cell}
:tags: [remove-input]
print(scene_stage.ExportToString(addSourceFileComment=False))
```

### Example 2: Automatic timeCodesPerSecond Scaling

This example demonstrates that USD **does** automatically handle `timeCodesPerSecond` differences during composition. We'll create an animated asset at 60 fps and reference it into a 24 fps scene.

```{code-cell}
:emphasize-lines: 8-10, 17-20, 25-27, 34-36, 52-55, 57-59, 63-67
from pxr import Usd, UsdGeom, Gf

# Create animated asset at 60 fps
anim_asset_path = "_assets/animated_60fps.usda"
anim_stage = Usd.Stage.CreateNew(anim_asset_path)
UsdGeom.SetStageUpAxis(anim_stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(anim_stage, 1.0)
anim_stage.SetTimeCodesPerSecond(60)  # 60 fps
anim_stage.SetStartTimeCode(0)
anim_stage.SetEndTimeCode(120)  # 2 seconds of animation at 60fps

# Create animated sphere
anim_sphere = UsdGeom.Sphere.Define(anim_stage, "/AnimatedSphere")
anim_sphere.GetRadiusAttr().Set(1.0)
anim_sphere.GetDisplayColorAttr().Set([(0.3, 0.9, 0.3)])

# Animate from left to right over 2 seconds (120 frames at 60fps)
xform_api = UsdGeom.XformCommonAPI(anim_sphere)
xform_api.SetTranslate(Gf.Vec3d(-5, 0, 0), Usd.TimeCode(0))
xform_api.SetTranslate(Gf.Vec3d(5, 0, 0), Usd.TimeCode(120))

anim_stage.SetDefaultPrim(anim_sphere.GetPrim())
anim_stage.Save()

print(f"Animation asset: {anim_stage.GetStartTimeCode()}-{anim_stage.GetEndTimeCode()} @ {anim_stage.GetTimeCodesPerSecond()} fps")
print(f"  -> Duration: {(anim_stage.GetEndTimeCode() - anim_stage.GetStartTimeCode() + 1) / anim_stage.GetTimeCodesPerSecond():.1f} seconds") 
print(f"  -> Animates from x=-5 to x=5\n")

# Create scene at 24 fps that references the 60fps animation
scene_24fps_path = "_assets/units_timecode_scene.usda"
scene_stage = Usd.Stage.CreateNew(scene_24fps_path)
UsdGeom.SetStageUpAxis(scene_stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(scene_stage, 1.0)
scene_stage.SetTimeCodesPerSecond(24)  # Scene is 24 fps
scene_stage.SetStartTimeCode(0)
scene_stage.SetEndTimeCode(48)  # 2 seconds at 24fps

world = UsdGeom.Xform.Define(scene_stage, "/World")
scene_stage.SetDefaultPrim(world.GetPrim())

# Create a floor
floor = UsdGeom.Cube.Define(scene_stage, "/World/Plane")
floor_xform_api = UsdGeom.XformCommonAPI(floor)
floor_xform_api.SetTranslate(Gf.Vec3d(0, -1, 0))
floor_xform_api.SetScale(Gf.Vec3f(10.0, 0.1, 4.0))

# Author the same animation in 24fps for comparison
local_anim = UsdGeom.Sphere.Define(scene_stage, "/World/LocalAnimation")
local_anim.GetRadiusAttr().Set(1.0)
local_anim.GetDisplayColorAttr().Set([(0.9, 0.3, 0.3)])

# Animate from left to right over 2 seconds (48 frames at 24fps)
xform_api = UsdGeom.XformCommonAPI(local_anim)
xform_api.SetTranslate(Gf.Vec3d(-5, 2, 0), Usd.TimeCode(0))
xform_api.SetTranslate(Gf.Vec3d(5, 2, 0), Usd.TimeCode(48))

# Reference thte 60fps animated sphere
ref_prim = scene_stage.DefinePrim("/World/ReferencedAnimation")
ref_prim.GetReferences().AddReference(anim_asset_path)

scene_stage.Save()

print(f"Scene: {scene_stage.GetStartTimeCode()}-{scene_stage.GetEndTimeCode()} @ {scene_stage.GetTimeCodesPerSecond()} fps")
print(f"  -> Duration: {(scene_stage.GetEndTimeCode() - scene_stage.GetStartTimeCode() + 1) / scene_stage.GetTimeCodesPerSecond():.1f} seconds")
print(f"  -> Local sphere animates from x=-5 to x=5 like the referenced sphere")
print(f"  -> Referenced animation automatically scaled from 60fps to 24fps")
print(f"  -> Same 2-second duration and motion maintained")
```

```{code-cell}
:tags: [remove-input]
DisplayUSD(scene_24fps_path, show_usd_code=True)
```

The referenced animation plays back correctly in the 24 fps scene even though it was authored at 60 fps. USD automatically scales the time samples via value resolution. Both spheres take 2 seconds to complete and traverse the same distance, demonstrating that temporal scaling is handled automatically—unlike geometric units which require manual correction.

## Key Takeaways

Understanding USD's unit system is critical for building robust production pipelines:

1. **Different metadata, different rules**: `timeCodesPerSecond` is automatically reconciled during composition, while `metersPerUnit`, `kilogramsPerUnit`, and `upAxis` are not. Pipelines must handle geometric and physics unit mismatches explicitly.

2. **Standards and conventions are essential**: The most effective approach is establishing and enforcing organization-wide unit conventions during asset creation. This minimizes the need for runtime conversions and reduces the chance of errors.

3. **Pipeline responsibility**: When different units are unavoidable (e.g., ingesting external vendor assets), pipelines must apply corrective transforms or conversions to ensure consistent interpretation across the composed scene.

4. **Validation is key**: Implement validation tools that check for unit consistency across referenced assets and flag potential issues before they cause problems in production.

By understanding these distinctions and establishing clear unit handling strategies, you can build reliable USD pipelines that seamlessly integrate content from diverse sources while maintaining spatial and temporal accuracy.

