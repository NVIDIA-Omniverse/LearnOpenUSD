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

A simulation cache can run to thousands of frames, each written as its own file. You cannot reasonably make each one a {term}`sublayer <Sublayer>` — the {term}`layer stack <Layer Stack>` would be thousands of layers deep, and {term}`composition <Composition>` would have to resolve every one of them just to open the {term}`stage <Stage>`.

{term}`Value clips <Value Clips>` are OpenUSD's answer. A clip set points a {term}`prim <Prim>` at a sequence of external layers and pulls {term}`time samples <Time Sample>` out of whichever one covers the requested {term}`time code <Time Code>`.

## What Are Value Clips?

The key idea is that clips are **not a {term}`composition arc <Composition Arcs>`**. They bring in no prim structure, no {term}`metadata <Metadata>`, and no {term}`default values <Default Value>` — OpenUSD deliberately ignores all of that inside a clip for the sake of scalability. Clips participate only in {term}`value resolution <Value Resolution>`, supplying time-varying {term}`attribute <Attribute>` values and nothing else.

That also places them precisely: as [Value Resolution](./value-resolution.md) covers, at a single site OpenUSD consults time samples, then {term}`animation splines <Animation Spline>`, then the default value, then value clips. A `default` authored at the same site wins over the clips beneath it.

## The Three Pieces

A working setup has three parts.

**Clip layers** hold the animated data — flat time samples on a prim, nothing else. Every clip in a set uses the same prim name internally, and that name does **not** have to match the prim you are applying them to. That indirection is what lets one set of crowd animation drive many different character models.

**The manifest** is a small layer listing which attributes have animated data in the clips. OpenUSD reads it during value resolution so it does not have to open and inspect every clip file.

**The clip set** is dictionary-valued metadata on the target prim tying the two together.

```{note}
Clip metadata lives in a `clips` dictionary keyed by clip set name, so one prim can carry several named clip sets. The Python API defaults to a set named `default`. Inside the dictionary the keys are `assetPaths`, `primPath`, `active`, `times`, and `manifestAssetPath` — without the `clip` prefix that the `Usd.ClipsAPI` method names use.
```

## Which Fields Are Required

This is worth being precise about, because getting it wrong produces no error at all.

| Field | Required? | Purpose |
| --- | --- | --- |
| `assetPaths` | **yes** | Ordered list of clip layers |
| `primPath` | **yes** | Prim path to read inside the clips |
| `active` | **yes** | `(stageTime, clipIndex)` pairs — which clip is live when |
| `times` | no | `(stageTime, clipTime)` pairs for retiming; identity if omitted |
| `manifestAssetPath` | no | Path to the manifest; generated in memory if omitted |

```{caution}
Omit any of the three required fields and the clip set contributes **nothing at all**: `GetTimeSamples()` returns `[]`, every `Get()` returns `None`, and OpenUSD writes **zero bytes to stderr**. There is no exception and no warning. If clips appear to do nothing, check that all three are authored before looking anywhere else.
```

## The Manifest Is a Filter, Not Just an Index

The manifest is optional, but it does more than speed things up.

Omit `manifestAssetPath` and OpenUSD generates the manifest in memory by opening and inspecting the clip layers — correct, but it pays that cost at runtime. Author one, and it becomes authoritative: **an attribute the manifest does not declare will not resolve from clips**, even when the clip layers plainly contain samples for it. An empty manifest silently disables every attribute in the set.

Generate one rather than hand-writing it, with `Usd.ClipsAPI.GenerateClipManifest()` or the `usdstitchclips` command line tool, then point `manifestAssetPath` at the result.

```{note}
Inside a manifest, `double size.timeSamples = {}` means "this attribute has time samples in the clips". That is the opposite of what the same text means in an ordinary layer, where an empty `timeSamples` block is treated as no authored opinion.
```

## Retiming With `times`

`active` says *which* clip is live at a given stage time. `times` says *where inside that clip* to read, as a list of `(stageTime, clipTime)` pairs. OpenUSD interpolates between the pairs, so the mapping is a piecewise-linear curve from stage time to clip time.

That one field is what lets a single cache drive many differently-timed instances. Leaving `times` out gives you the identity mapping, so stage time is fed to the clip unchanged and the clip's own sample times must already be in stage time.

| `times` | Effect |
| --- | --- |
| `[(0, 0), (24, 24)]` | Identity — plays at authored speed |
| `[(0, 0), (48, 24)]` | Half speed — 24 frames of clip stretched over 48 |
| `[(0, 0), (12, 0), (36, 24)]` | Holds for 12 frames, then plays |
| `[(0, 24), (24, 0)]` | Plays in reverse |

```{note}
Retiming is only available on explicit clip sets. Template clips derive their timing from the file numbering and always use an identity mapping, which is the main reason to prefer the explicit form when you need offsets.
```

## Template Clips

When clips are a numbered sequence — the normal case for a simulation cache — you can skip `assetPaths` and `active` entirely and describe the sequence with a pattern instead:

```python
api.SetClipTemplateAssetPath("./cache.###.usda")
api.SetClipTemplateStartTime(1)
api.SetClipTemplateEndTime(10)
api.SetClipTemplateStride(1)
api.SetClipPrimPath("/Cache")
```

The `#` characters are a minimum field width, so `cache.###.usda` matches `cache.001.usda`. The number in the filename *is* a stage time code, which means each clip's internal samples must be authored in stage time.

Template clips are more compact but less capable: they cannot scale, loop, or reverse, because there is no `times` mapping to express that. If a clip set authors both template and explicit fields, **the explicit fields win and the template ones are ignored**.

```{caution}
`GetClipTemplateStartTime()`, `GetClipTemplateEndTime()`, `GetClipTemplateStride()` and `GetClipTemplateActiveOffset()` return **uninitialized garbage** when the field has not been authored — a subnormal value like `6.27e-310`, with no exception and no way to tell it apart from a real number. Check `"templateStartTime" in api.GetClips()["default"]` before trusting them.
```

## Examples

```{tip}
You can run these examples locally as Jupyter notebooks. See [How to Run Notebooks Locally](../jupyter-notebook-setup.md) for setup instructions.
```

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
:test-tags: [value-clips-setup]
import os

from pxr import Gf, Usd, UsdGeom, Sdf

from lousd.utils.visualization import DisplayUSD

# Clips are referenced by asset path, so these examples need real files.
ASSETS = os.path.abspath("_assets/clips")
os.makedirs(ASSETS, exist_ok=True)


def asset_path(name):
    return os.path.join(ASSETS, name)


def fresh_layer(name):
    """Return an empty layer at this path, safe to call on a re-run.

    Sdf.Layer.CreateNew refuses if the file exists on disk OR if a layer with
    that identifier is already open, so handle both cases.
    """
    path = asset_path(name)
    existing = Sdf.Layer.Find(path)
    if existing is not None:
        existing.Clear()
        return existing
    if os.path.exists(path):
        os.remove(path)
    return Sdf.Layer.CreateNew(path)


def make_clip(name, samples):
    """Write one clip layer holding time samples for /Clip.size."""
    layer = fresh_layer(name)
    stage = Usd.Stage.Open(layer)
    attr = stage.DefinePrim("/Clip").CreateAttribute("size", Sdf.ValueTypeNames.Double)
    for time, value in samples.items():
        attr.Set(value, time)
    layer.Save()
    return layer


def sample(attr, times):
    return {t: attr.Get(t) for t in times}
```

### Example 1: A Working Clip Set

Two clip layers, each holding samples at its own local times 0 and 1. The clip set makes the first active from stage time 0 and the second from stage time 2, and `times` maps each two-unit stage window onto the clip's local 0..1 range.

```{code-cell}
:test-tags: [value-clips-minimal]
:emphasize-lines: 14-19

from pxr import Usd, Sdf

make_clip("clip_a.usda", {0: 0.0, 1: 1.0})
make_clip("clip_b.usda", {0: 10.0, 1: 11.0})

root = fresh_layer("root.usda")
stage: Usd.Stage = Usd.Stage.Open(root)
thing = stage.DefinePrim("/World/Thing", "Xform")

# The attribute must be declared on the prim itself
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

The composed attribute behaves like ordinary animation — interpolation works between samples — but the values are coming out of two separate files that were never sublayered or referenced.

### Example 2: The Manifest Decides What Resolves

The same clips, three times over: no manifest, a manifest that declares `size`, and a manifest that declares nothing.

```{code-cell}
:test-tags: [value-clips-manifest]
:emphasize-lines: 20-22

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

No manifest works — OpenUSD inspects the clips itself. A manifest that declares `size` works. A manifest that declares nothing produces **no samples and no value**, with nothing written to stderr. The manifest is authoritative once you author one.

### Example 3: Every Required Field Fails Silently

Omitting each required field in turn, with stderr captured so you can see how much OpenUSD says about it.

```{code-cell}
:test-tags: [value-clips-silent-failure]
:emphasize-lines: 26-27

import contextlib
import io

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
    captured = io.StringIO()
    with contextlib.redirect_stderr(captured):
        omission_stages[missing] = build_omitting(missing)
        attr = omission_stages[missing].GetAttributeAtPath("/World/Thing.size")
        samples, value = attr.GetTimeSamples(), attr.Get(0)
    omission_results[missing] = (samples, value, len(captured.getvalue()))
    label = missing or "(nothing omitted)"
    print(f"omit {label:18} samples={str(samples):22} value={str(value):6} stderr={len(captured.getvalue())} bytes")
```

Every failure is total and completely quiet. This is the single most common way a clip set goes wrong, and OpenUSD gives you nothing to go on.

### Example 4: Seeing the Offsets

Numbers only get you so far. Here three cubes read from **the same single clip layer** and differ only in their `times` mapping, so the retiming is visible directly.

```{code-cell}
:test-tags: [value-clips-retiming]
:emphasize-lines: 24-26

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

All three cubes are reading the identical clip. `FullSpeed` finishes its slide by frame 24, `HalfSpeed` takes twice as long because 24 frames of clip data are stretched across 48, and `Delayed` sits still for 12 frames because its mapping holds clip time at 0 before advancing.

```{note}
The viewer flattens the stage before converting it for display, and flattening bakes resolved clip values into ordinary time samples. That is why clip-driven motion animates here with no extra work, unlike {term}`animation splines <Animation Spline>`, which need `bake_splines_for_display=True`.
```

## Failure Modes Worth Knowing

| What you did | What you see |
| --- | --- |
| Omitted `assetPaths`, `primPath`, or `active` | No samples, no values, no message |
| Authored a manifest that omits the attribute | Same — silent and total |
| Did not declare the attribute on the prim | Values resolve at exact sample times, but **any interpolated time raises** "Unknown value type" |
| Declared the attribute with the wrong type | Correct values at exact sample times, `None` everywhere in between, silently |
| `primPath` points at a prim not in the clips | Silent — falls back to a default or schema fallback if one exists, otherwise `None` |
| A clip file listed in `assetPaths` is missing | Warns on stderr, and only the times that clip served return `None` |

The pattern is that structural mistakes are silent while missing files are not. When clips produce nothing, start by checking the three required fields and the manifest.

## Key Takeaways

Value clips let a prim source time-varying values from a sequence of external layers without those layers entering composition at all. They bring in values and nothing else — no prims, no metadata, no defaults — which is what makes them scale to caches that a layer stack could never hold.

Three things are worth carrying forward. **A clip set needs `assetPaths`, `primPath`, and `active`**, and omitting any one disables it without a word. **The manifest is a filter**: optional, but authoritative once authored, so an attribute it omits will not resolve. And **the attribute must be declared on the target prim**, or interpolated queries raise rather than return.

For numbered sequences, template clips are the compact form, at the cost of retiming — and be wary of the template getters, which return uninitialized memory for fields you never authored.
