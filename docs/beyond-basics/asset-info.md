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
# Asset Info

## What Is Asset Info?

{term}`Asset info <Asset Info>` is a {term}`metadata <Metadata>` dictionary that records where a piece of scene description came from. When a {term}`prim <Prim>` is published from an asset management system, `assetInfo` is where you stamp the identity of that {term}`asset <Asset>`: what it is called, which revision it is, and how to find it again.

The most important thing to understand about `assetInfo` is that it is *descriptive*, not *functional*. Authoring it does not make {term}`referencing <Reference>` work and does not cause OpenUSD to load anything. It is a standardized place to record provenance so that every pipeline does not have to invent its own convention for the same information.

This matters once assets start moving between teams and organizations. A composed {term}`stage <Stage>` tells you what the data *is*, but not which published revision of which asset it came from. Asset info carries that answer along with the data.

## How Does It Work?

`assetInfo` is defined on {usdcpp}`UsdObject`, which means it can be authored on prims *and* on {term}`properties <Property>`. It behaves like any other dictionary-valued metadata: you can put arbitrary keys in it, and it is composed along with the prim it lives on.

### The Conventional Fields

Any key is legal, but four have an agreed-upon meaning and direct API access through {usdcpp}`UsdModelAPI`:

| Field | Type | Purpose |
| --- | --- | --- |
| `identifier` | `asset` | The asset path this content came from |
| `name` | `string` | The asset's name in your asset database |
| `version` | `string` | The revision the data was published at |
| `payloadAssetDependencies` | `asset[]` | Pre-computed dependencies, so tools can inspect them without loading the {term}`payload <Payload>` |

Because `identifier` is a genuine `asset`-typed value, it participates in {term}`asset resolution <Asset Resolution>` the same way a reference path does: relative paths are anchored to the {term}`layer <Layer>` that authored them.

`payloadAssetDependencies` is worth calling out because it exists to solve a specific performance problem. Walking an asset's dependencies normally means loading its payloads. Publishing the dependency list up onto the interface prim lets tooling answer "what does this asset need?" without paying that cost, which is the same lofting idea covered in [Reference/Payload Pattern](../asset-structure/reference-payload-pattern/what-is-ref-payload-pattern.md).

### How Asset Info Composes

Dictionary metadata composes *per key*, not as a single value. If a downstream {term}`layer <Layer>` authors `assetInfo` with only a `version` key, it overrides `version` and leaves the other keys from the referenced asset intact.

This is what makes the field usable in practice. A shot layer can stamp a version bump without having to restate an asset's identity, and without accidentally erasing the fields it did not set.

```{note}
That per-key composition is convenient, but it is not free. As noted in [Custom Properties](./custom-properties.md), composable dictionary metadata costs more to compose than a plain {term}`attribute <Attribute>`. Use `assetInfo` for the asset identity it was designed for, and reach for custom properties when you need general-purpose user data.
```

## Working With Python

There are two ways to reach the same data. {usdcpp}`UsdModelAPI` gives you typed accessors for the four conventional fields:

```python
from pxr import Usd, Sdf

model = Usd.ModelAPI(prim)
model.SetAssetIdentifier(Sdf.AssetPath("asset://chairs/chair_a.usd"))
model.SetAssetName("chair_a")
model.SetAssetVersion("v003")
```

{usdcpp}`UsdObject` gives you raw dictionary access, which is how you author your own keys:

```python
prim.SetAssetInfoByKey("department", "set_dress")
prim.GetAssetInfo()          # the whole dictionary
prim.HasAuthoredAssetInfo()  # was any of it authored here?
prim.ClearAssetInfoByKey("department")
```

Note that `SetAssetInfoByKey` sets a single key without disturbing the others, while `SetAssetInfo` replaces the entire dictionary.

## Examples

```{tip}
You can run these examples locally as Jupyter notebooks. See [How to Run Notebooks Locally](../jupyter-notebook-setup.md) for setup instructions.
```

+++
```{include} ../_includes/hidden-create-new-stage-import-note.md
```
+++
```{code-cell}
:tags: [remove-input]
:test-tags: [asset-info-setup]
from lousd.utils.visualization import DisplayCode
from lousd.utils.helperfunctions import create_new_stage
```

### Example 1: Stamping Asset Info on a Published Asset

Here we build a small component asset and record its identity on the entry point prim. In a real pipeline these values would come from your asset management system at publish time rather than being typed in by hand.

```{code-cell}
:test-tags: [asset-info-author]
:emphasize-lines: 11-18

from pxr import Usd, UsdGeom, Sdf

file_path = "_assets/chair_a.usda"
stage: Usd.Stage = create_new_stage(file_path)

# Build the asset's entry point prim and make it the default prim
chair: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/chair_a")
stage.SetDefaultPrim(chair.GetPrim())
UsdGeom.Cube.Define(stage, chair.GetPath().AppendPath("Geometry"))

# Use UsdModelAPI for the four conventional fields
model = Usd.ModelAPI(chair.GetPrim())
model.SetAssetIdentifier(Sdf.AssetPath("asset://chairs/chair_a.usd"))
model.SetAssetName("chair_a")
model.SetAssetVersion("v003")

# Any additional key you need can go in the same dictionary
chair.GetPrim().SetAssetInfoByKey("department", "set_dress")

stage.Save()
print(chair.GetPrim().GetAssetInfo())
```
```{code-cell}
:tags: [remove-input]
DisplayCode(file_path)
```

Notice how `assetInfo` is serialized as a dictionary on the prim, with `identifier` written using OpenUSD's `@...@` asset path syntax.

### Example 2: Asset Info Travels Through a Reference

Now we reference that asset into a scene. The asset info composes through the reference, so the consuming stage can see exactly which asset and revision it picked up.

```{code-cell}
:test-tags: [asset-info-through-reference]
:emphasize-lines: 12-15

from pxr import Usd

scene_path = "_assets/asset_info_scene.usda"
scene: Usd.Stage = create_new_stage(scene_path)

world = scene.DefinePrim("/World", "Xform")
scene.SetDefaultPrim(world)

chair_1 = scene.DefinePrim("/World/Chair_1", "Xform")
chair_1.GetReferences().AddReference("./chair_a.usda")

# The asset info came along with the reference, even though
# nothing was authored for it in this layer
print("Composed asset info:", chair_1.GetAssetInfo())
print("Authored in this layer?", chair_1.HasAuthoredAssetInfo())

scene.Save()
```

`HasAuthoredAssetInfo` reports `True` here because the referenced layer authored it. Use it to check whether asset info exists at all, not to test whether *this particular layer* is the one that set it.

### Example 3: Overriding a Single Field

Finally, we bump the version on the referencing prim. Because dictionary metadata composes per key, the fields we do not touch survive.

```{code-cell}
:test-tags: [asset-info-per-key-override]
:emphasize-lines: 9-10

from pxr import Usd

scene_path = "_assets/asset_info_scene.usda"
scene: Usd.Stage = Usd.Stage.Open(scene_path)
chair_1 = scene.GetPrimAtPath("/World/Chair_1")

print("Before:", chair_1.GetAssetInfo())

# Override only the version key
chair_1.SetAssetInfoByKey("version", "v004")

composed = chair_1.GetAssetInfo()
print("After: ", composed)
print()
print("version was overridden:", composed["version"])
print("name survived from the referenced asset:", composed["name"])
print("department survived too:", composed["department"])

scene.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayCode(scene_path)
```

Only `version` appears in this layer's scene description, but the composed value still carries all four keys. If we had used `SetAssetInfo` with a dictionary containing just `version`, we would have replaced the whole dictionary in this layer instead and lost the ability to see the rest of the identity downstream.

## Key Takeaways

Asset info is OpenUSD's standard place to record asset provenance: which asset a prim came from, what it is called, and which revision was published. It is a dictionary on {usdcpp}`UsdObject`, so it works on prims and properties alike, and it composes per key so downstream layers can update one field without restating the others.

It is worth being clear about what asset info does *not* do. It records a version, but it does not manage one; nothing validates that the stamped value matches what actually composed, so it is only as trustworthy as the process that wrote it. Outside of `payloadAssetDependencies`, which exists as a hint for dependency-analysis tooling, OpenUSD itself does not act on these fields. They are a convention that your pipeline is responsible for writing and honoring.
