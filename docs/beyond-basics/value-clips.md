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
# Value Clips

## What Are Value Clips?

{term}`Value clips <Value Clips>` let you assemble {term}`time-sampled <Time Sample>` attribute values from a sequence of external {term}`layers <Layer>`. They are useful for simulation caches and other large animation datasets, where each file may contain only a portion of the animation.

Clip layers are opened as their values are needed. This avoids adding every cache file to the {term}`layer stack <Layer Stack>` and processing those layers during {term}`composition <Composition>`. Using {term}`sublayers <Sublayer>` alone also does not join the samples: the strongest layer with time samples for an attribute supplies its animation.

In this lesson, you will configure a clip set, reuse its animation with different timing, and check which attributes receive clip values.

## How Does It Work?

Value clips participate in {term}`value resolution <Value Resolution>`. They supply animated values for {term}`attributes <Attribute>` already defined on the {term}`stage <Stage>`, either through authored declarations or a schema. Clip layers do not introduce prim structure, {term}`metadata <Metadata>`, or {term}`default values <Default Value>` into the stage.

As described in [Value Resolution](./value-resolution.md), OpenUSD checks time samples, then {term}`animation splines <Animation Spline>`, then defaults, then clips at a given location in the composition. A default authored at the same location takes precedence over clip values.

### Clip Layers, Manifests, and Clip Sets

A value clip setup uses three related pieces:

- **Clip layers** store the animated data. A shared prim path identifies the data to read in each clip. It can differ from the target {term}`prim <Prim>` path on the stage, allowing the same clip data to drive multiple prims.
- **The manifest** declares which attributes have animation in the clips. OpenUSD uses it to determine whether an attribute can receive clip values without inspecting every clip file.
- **The clip set** stores metadata on a prim that identifies the clip layers, their timing, and the manifest.

Clip metadata is stored in a `clips` dictionary keyed by clip set name. A prim can have multiple clip sets; the Python API uses a set named `default` unless you specify another name.

## Working With Python

Use `Usd.ClipsAPI(prim)` to configure a clip set. The following table lists the metadata fields for an explicit clip set, which specifies the clip files and their activation times directly. The API methods add a `Clip` prefix to these field names, as in `SetClipAssetPaths()`.

| Field | Required? | Purpose |
| --- | --- | --- |
| `assetPaths` | Yes | Ordered list of clip layers |
| `primPath` | Yes | Prim path to read inside the clips |
| `active` | Yes | `(stageTime, clipIndex)` pairs identifying when each clip is active |
| `times` | No | `(stageTime, clipTime)` pairs for retiming; identity if omitted |
| `manifestAssetPath` | No | Path to the manifest; generated in memory if omitted |

### Declaring Attributes in a Manifest

If you omit `manifestAssetPath`, OpenUSD generates a manifest by opening and inspecting the clip layers. For large clip sets, you can avoid this work at runtime by generating and saving a manifest with `Usd.ClipsAPI.GenerateClipManifest()` or the `usdstitchclips` command line tool, then setting `manifestAssetPath` to that file.

An authored manifest determines which attributes can receive values from the clip set. It must declare each attribute you want to read, even if the clip files already contain samples for that attribute. A declaration such as `double size` is sufficient; the manifest does not need to duplicate the animation samples.

### Retiming With `times`

The `active` field selects the clip to use at a given stage {term}`time code <Time Code>`. The `times` field maps that stage time to a time within the clip using `(stageTime, clipTime)` pairs. OpenUSD interpolates linearly between these pairs.

You can use this mapping to reuse animation at different speeds or with a delayed start. If you omit `times`, the mapping is identity: stage time is passed to the clip unchanged.

| `times` | Effect |
| --- | --- |
| `[(0, 0), (24, 24)]` | Plays at the authored speed |
| `[(0, 0), (48, 24)]` | Stretches 24 frames of clip data across 48 stage frames |
| `[(0, 0), (12, 0), (36, 24)]` | Holds for 12 frames, then plays |
| `[(0, 24), (24, 0)]` | Plays in reverse |

### Template Clips

For regularly numbered files, template metadata provides a compact way to specify a clip sequence. OpenUSD derives the asset paths and timing from the pattern, start time, end time, and stride:

```python
api.SetClipTemplateAssetPath("./cache.###.usda")
api.SetClipTemplateStartTime(1)
api.SetClipTemplateEndTime(10)
api.SetClipTemplateStride(1)
api.SetClipPrimPath("/Cache")
```

The `#` characters specify the minimum padding width, so `cache.###.usda` selects names such as `cache.001.usda`. The generated timing uses an identity mapping in the layer's time coordinates, so the sample times inside each clip should match the numbered sequence.

Use an explicit clip set when you need a custom `times` mapping, such as a hold or a loop. Template clips derive their mapping from the sequence, but you can still shift and scale their playback with {term}`layer offsets <Layer Offset>` on a reference or sublayer. See [Layer Offsets in the value clips documentation](https://openusd.org/release/api/_usd__page__value_clips.html#Usd_ValueClips_ClipValueResolution_LayerOffsets) for how offsets apply to both forms. If you author both template and explicit clip metadata, OpenUSD prefers the explicit form.

## Examples

```{tip}
You can run these examples locally as Jupyter notebooks. See [How to Run Notebooks Locally](../jupyter-notebook-setup.md) for setup instructions. Run the examples in order; later examples reuse the clip files created in Example 1.
```

+++ {"tags": ["remove-cell"]}
>**NOTE**: Run the following setup cell before starting the examples. It imports the display helper and prepares the directory and layer helpers used below.
+++
```{code-cell}
:tags: [remove-input]
:test-tags: [value-clips-setup]
import os

from pxr import Sdf

from lousd.utils.visualization import DisplayUSD

# Clips are referenced by asset path, so these examples need real files.
ASSETS = os.path.abspath("_assets/clips")
os.makedirs(ASSETS, exist_ok=True)


def asset_path(name):
    return os.path.join(ASSETS, name)


def fresh_layer(name):
    """Return an empty layer at this path, safe to call on a re-run.

    Reuse an open layer when possible and remove an existing file before
    creating a new layer so repeated runs start with the same content.
    """
    path = asset_path(name)
    existing = Sdf.Layer.Find(path)
    if existing is not None:
        existing.Clear()
        return existing
    if os.path.exists(path):
        os.remove(path)
    return Sdf.Layer.CreateNew(path)


def sample(attr, times):
    return {t: attr.Get(t) for t in times}
```

### Example 1: A Working Clip Set

First, we create two clip layers, each with samples at local times 0 and 1. The `make_clip()` function authors a `size` attribute at `/Clip` and saves its samples to a file. The setup cell defines `fresh_layer()` to create an empty layer under `_assets/clips/`, including when you rerun the notebook.

```{code-cell}
:test-tags: [value-clips-minimal]
from pxr import Usd, Sdf


def make_clip(name, samples):
    """Write one clip layer holding time samples for /Clip.size."""
    layer = fresh_layer(name)
    stage = Usd.Stage.Open(layer)
    attr = stage.DefinePrim("/Clip").CreateAttribute("size", Sdf.ValueTypeNames.Double)
    for time, value in samples.items():
        attr.Set(value, time)
    layer.Save()
    return layer
```

Next, we declare the attribute on the target prim and configure the clip set. The first clip is active before stage time 2, and the second is active from time 2 onward. The `times` mapping maps stage times 0–1 to the first clip's local times 0–1 and stage times 2–3 to the second clip's local times 0–1.

```{code-cell}
:test-tags: [value-clips-minimal]
:emphasize-lines: 13-18

from pxr import Usd, Sdf

make_clip("clip_a.usda", {0: 0.0, 1: 1.0})
make_clip("clip_b.usda", {0: 10.0, 1: 11.0})

root = fresh_layer("root.usda")
stage: Usd.Stage = Usd.Stage.Open(root)
thing = stage.DefinePrim("/World/Thing", "Xform")

# Declare the attribute on the stage; clips supply its animated values
size = thing.CreateAttribute("size", Sdf.ValueTypeNames.Double)

api = Usd.ClipsAPI(thing)
api.SetClipAssetPaths([Sdf.AssetPath("./clip_a.usda"), Sdf.AssetPath("./clip_b.usda")])
api.SetClipPrimPath("/Clip")
api.SetClipActive([(0, 0), (2, 1)])
# Map stage 0..1 onto clip time 0..1, then stage 2..3 onto clip time 0..1 again
api.SetClipTimes([(0, 0), (1, 1), (2, 0), (3, 1)])

print("time samples:", size.GetTimeSamples())
print("values      :", sample(size, [0, 0.5, 1, 2, 2.5, 3]))
print()
print(root.ExportToString())
```

You can query and interpolate the composed attribute as you would other animated attributes. Its time samples come from the two clip files, which are accessed during value resolution.

### Example 2: Retiming a Shared Clip

This example applies one animation clip to three cubes. Each cube uses a different `times` mapping so you can compare normal playback, half-speed playback, and a delayed start.

```{code-cell}
:test-tags: [value-clips-retiming]
:emphasize-lines: 25-29

from pxr import Gf, Usd, UsdGeom, Sdf

# One clip layer: a slide from x=0 to x=6 over the clip's own frames 0..24
slide = fresh_layer("slide.usda")
slide_stage = Usd.Stage.Open(slide)
slide_op = UsdGeom.Xformable(slide_stage.DefinePrim("/Clip", "Xform")).AddTranslateOp()
slide_op.Set(Gf.Vec3d(0, 0, 0), 0)
slide_op.Set(Gf.Vec3d(6, 0, 0), 24)
slide.Save()

offsets = fresh_layer("offsets.usda")
offset_stage: Usd.Stage = Usd.Stage.Open(offsets)
offset_stage.SetStartTimeCode(0)
offset_stage.SetEndTimeCode(48)
world = UsdGeom.Xform.Define(offset_stage, "/World")
offset_stage.SetDefaultPrim(world.GetPrim())


def clipped_cube(name, row, times):
    cube = UsdGeom.Cube.Define(offset_stage, f"/World/{name}")
    cube.GetSizeAttr().Set(1.0)
    xformable = UsdGeom.Xformable(cube)
    xformable.AddTranslateOp()                                        # driven by clips
    xformable.AddTranslateOp(opSuffix="row").Set(Gf.Vec3d(0, row, 0))  # static, separates the rows
    api = Usd.ClipsAPI(cube.GetPrim())
    api.SetClipAssetPaths([Sdf.AssetPath("./slide.usda")])
    api.SetClipPrimPath("/Clip")
    api.SetClipActive([(0, 0)])
    api.SetClipTimes(times)
    return cube.GetPrim().GetAttribute("xformOp:translate")


full = clipped_cube("FullSpeed", 0.0, [(0, 0), (24, 24)])
half = clipped_cube("HalfSpeed", 2.0, [(0, 0), (48, 24)])
delayed = clipped_cube("Delayed", 4.0, [(0, 0), (12, 0), (36, 24)])
offsets.Save()

retiming_results = {}
print("frame   FullSpeed  HalfSpeed  Delayed")
for frame in (0, 12, 24, 36, 48):
    row = (full.Get(frame)[0], half.Get(frame)[0], delayed.Get(frame)[0])
    retiming_results[frame] = row
    print(f"{frame:5}   {row[0]:8.2f}   {row[1]:8.2f}   {row[2]:7.2f}")
```

```{code-cell}
:tags: [remove-input]
# DisplayUSD needs a path relative to the lesson, not the absolute one asset_path builds,
# because it is written straight into the page's <model-viewer> src attribute.
DisplayUSD("_assets/clips/offsets.usda", show_usd_code=True)
```

`FullSpeed` finishes moving by frame 24. `HalfSpeed` stretches the same motion across 48 frames. `Delayed` holds clip time at 0 for the first 12 frames, then plays the motion through frame 36. Each cube uses the same clip data; only the timing metadata changes.

```{note}
The viewer flattens the stage before converting it for display. Flattening converts resolved clip values to ordinary time samples, which the viewer can play back.
```

### Example 3: Selecting Attributes With a Manifest

We now compare three configurations using the clips from Example 1: an automatically generated manifest, an authored manifest that declares `size`, and an empty manifest.

```{code-cell}
:test-tags: [value-clips-manifest]
:emphasize-lines: 22-23

from pxr import Usd, Sdf

# A manifest declaring size, and one declaring nothing at all
good = fresh_layer("manifest_good.usda")
mstage = Usd.Stage.Open(good)
mstage.OverridePrim("/Clip").CreateAttribute("size", Sdf.ValueTypeNames.Double)
good.Save()

empty = fresh_layer("manifest_empty.usda")
empty.Save()


def build(manifest, tag):
    layer = fresh_layer(f"root_{tag}.usda")
    stage = Usd.Stage.Open(layer)
    prim = stage.DefinePrim("/World/Thing", "Xform")
    prim.CreateAttribute("size", Sdf.ValueTypeNames.Double)
    api = Usd.ClipsAPI(prim)
    api.SetClipAssetPaths([Sdf.AssetPath("./clip_a.usda"), Sdf.AssetPath("./clip_b.usda")])
    api.SetClipPrimPath("/Clip")
    api.SetClipActive([(0, 0), (2, 1)])
    if manifest:
        api.SetClipManifestAssetPath(Sdf.AssetPath(f"./{manifest}"))
    # Return the stage, not the attribute: an attribute handle expires when the
    # stage it came from is garbage collected.
    return stage


manifest_results = {}
manifest_stages = {}
for manifest, tag in ((None, "none"), ("manifest_good.usda", "good"), ("manifest_empty.usda", "empty")):
    manifest_stages[tag] = build(manifest, tag)
    attr = manifest_stages[tag].GetAttributeAtPath("/World/Thing.size")
    manifest_results[tag] = (attr.GetTimeSamples(), attr.Get(0))
    print(f"manifest={tag:6} samples={str(attr.GetTimeSamples()):22} value at 0 = {attr.Get(0)}")
```

Both the generated manifest and the authored manifest that declares `size` allow the clip values to resolve. The empty manifest excludes `size` from the clip set. In this example, the attribute has no other value source, so it returns no time samples and `Get(0)` returns `None`.

### Example 4: Checking Required Fields

This example omits each required field in turn and queries the resulting attribute. Compare each result with the complete clip set to see whether it contributes values.

```{code-cell}
:test-tags: [value-clips-required-fields]
:emphasize-lines: 11-17

from pxr import Usd, Sdf

FIELDS = ["assetPaths", "primPath", "active"]


def build_omitting(missing):
    layer = fresh_layer(f"root_omit_{missing or 'nothing'}.usda")
    stage = Usd.Stage.Open(layer)
    prim = stage.DefinePrim("/World/Thing", "Xform")
    prim.CreateAttribute("size", Sdf.ValueTypeNames.Double)
    api = Usd.ClipsAPI(prim)
    if missing != "assetPaths":
        api.SetClipAssetPaths([Sdf.AssetPath("./clip_a.usda"), Sdf.AssetPath("./clip_b.usda")])
    if missing != "primPath":
        api.SetClipPrimPath("/Clip")
    if missing != "active":
        api.SetClipActive([(0, 0), (2, 1)])
    return stage


omission_results = {}
omission_stages = {}
for missing in [None] + FIELDS:
    omission_stages[missing] = build_omitting(missing)
    attr = omission_stages[missing].GetAttributeAtPath("/World/Thing.size")
    samples, value = attr.GetTimeSamples(), attr.Get(0)
    omission_results[missing] = (samples, value)
    label = missing or "(nothing omitted)"
    print(f"omit {label:18} samples={str(samples):22} value={value}")
```

Omitting any required field prevents this clip set from contributing values. Because the attribute has no other value source, its sample list is empty and `Get(0)` returns `None`.

Other value sources can still provide a result. For example, changing the prim's type to `Cube` makes the schema's fallback value for `size` available, even though the clip set is still missing `active`:

```{code-cell}
:test-tags: [value-clips-required-fields]
from pxr import UsdGeom

fallback_stage = omission_stages["active"]
fallback_prim = fallback_stage.GetPrimAtPath("/World/Thing")
fallback_prim.SetTypeName("Cube")
fallback_value = UsdGeom.Cube(fallback_prim).GetSizeAttr().Get(0)
print("size from the Cube schema fallback:", fallback_value)
```

## Troubleshooting Clip Values

If the expected animation is missing, check the clip set's fields, manifest, and attribute declarations. The table below distinguishes a clip set contributing no values from an attribute having no resolved value at all.

| Configuration | Result and next step |
| --- | --- |
| An explicit clip set omits `assetPaths`, `primPath`, or `active` | The clip set contributes no values. Check that all three fields are authored. |
| The manifest omits an attribute | The clip set does not supply that attribute. Include its declaration or regenerate the manifest. |
| The attribute is not defined on the composed stage | Clips do not create the attribute. Declare it on the stage or use a schema that defines it. |
| The attribute type differs from the type in the clips | Interpolation may fail. Use matching attribute types in the stage and clip layers. |
| `primPath` does not identify the data in the clips | The clip set does not supply the expected values. Check the path in the clip files. |
| A file listed in `assetPaths` is missing | OpenUSD reports a warning. Check the file path and asset resolution. |

When a clip set contributes no values, other sources, including authored values or schema fallbacks, can still resolve. In Example 4, the custom attribute returns `None` until the `Cube` schema provides a fallback.

```{note}
In tests with `usd-core` 25.11, omitting a required field or using an empty manifest produced no warning. Check the resolved values as well as diagnostics when troubleshooting.
```

```{note}
In `usd-core` 25.11, the Python getters `GetClipTemplateStartTime()`, `GetClipTemplateEndTime()`, `GetClipTemplateStride()`, and `GetClipTemplateActiveOffset()` can return an uninitialized numeric value when the field is absent. This is an implementation issue in that version's [Python wrapper](https://github.com/PixarAnimationStudios/OpenUSD/blob/v25.11/pxr/usd/usd/wrapClipsAPI.cpp), rather than a meaningful default. Check for the field before reading it, for example with `"templateStartTime" in api.GetClips().get("default", {})`.
```

## Key Takeaways

Value clips let you assemble animation from external layers while keeping prim and attribute definitions in the composed stage. A clip set identifies the data to read, its active intervals, and the mapping between stage time and clip time. Its manifest declares which attributes can receive clip values.

Use explicit clip metadata for custom timing and template metadata for regularly numbered sequences. Layer offsets can shift and scale either form. When expected clip values are missing, check the clip metadata and attribute declarations, and consider whether another source is providing the resolved value.
