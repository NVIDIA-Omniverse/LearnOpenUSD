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
# Edit Targets and Layer Muting

So far, when you have authored to a {term}`stage <Stage>`, your edits have quietly gone to one place: the root {term}`layer <Layer>`. In a real pipeline that is rarely what you want. A modeler's changes belong in the modeling layer, a shot override belongs in the shot layer, and a throwaway experiment belongs somewhere that never reaches disk.

This lesson covers the two controls that make that possible. The {term}`edit target <Edit Target>` decides *where your edits are written*. {term}`Layer muting <Layer Muting>` decides *which layers are read*. Together they let you steer authoring and isolate contributions without restructuring the {term}`layer stack <Layer Stack>`.

## What Is an Edit Target?

An edit target tells a stage which layer should receive authored {term}`opinions <Direct Opinion>`. Every stage always has one. Unless you change it, it is the root layer, which is why `Usd.Stage.CreateNew()` followed by authoring puts everything in that single file.

Changing the edit target does not change what the stage *shows* you. You still see the fully composed result. It only changes which layer your next edit is written into, and therefore how strong that edit is once {term}`composition <Composition>` resolves it.

```{important}
An edit target does not override strength ordering. Authoring into a weak layer writes a weak opinion, so a stronger layer can still win. If an edit appears to do nothing, check where it landed before assuming the API failed.
```

## What Is Layer Muting?

Muting a layer removes its contributions from composition without deleting the layer or editing the layer stack that refers to it. The layer keeps its data; the stage simply stops reading it.

The critical property is that muting is **stage-level state, not scene description**. It is not recorded in any layer, it is not saved, and another stage opened on the same root layer will not see it. That makes muting safe for exactly the things you would not want to persist: bisecting which layer introduced a bad opinion, checking what a scene looks like without the lighting department's contributions, or skipping an expensive layer while iterating.

## Working With Python

The recommended way to change the edit target is {usdcpp}`UsdEditContext`, a context manager that restores the previous target when the block exits:

```python
from pxr import Usd

# Author into a specific layer, then go back to whatever was set before
with Usd.EditContext(stage, some_layer):
    prim.GetAttribute("radius").Set(5.0)
```

You can also set it directly with `stage.SetEditTarget(layer)` and read it back with `stage.GetEditTarget()`, but then restoring the previous target is your responsibility. Prefer the context manager.

Muting is driven from the stage using layer identifiers:

```python
stage.MuteLayer(layer.identifier)
stage.UnmuteLayer(layer.identifier)
stage.IsLayerMuted(layer.identifier)
stage.GetMutedLayers()

# Batch several changes into a single recomposition
stage.MuteAndUnmuteLayers([mute_layer.identifier], [unmute_layer.identifier])
```

Each mute or unmute triggers a recomposition, so use {usdcpp}`UsdStage::MuteAndUnmuteLayers` when changing several layers at once rather than calling `MuteLayer` in a loop.

```{caution}
Muting matches on the layer **identifier string**, and it fails silently. If the identifier you pass does not match the one the stage resolved for that layer, `GetMutedLayers` will happily report your string while composition is completely unaffected.

This bites most often with relative paths: a layer opened as `./shot.usda` and the same file opened as an absolute path are two different identifier strings. When muting does nothing, compare your identifier against `stage.GetLayerStack()` before looking anywhere else.
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
:test-tags: [edit-targets-setup]
import os
from pxr import Sdf
from lousd.utils.visualization import DisplayCode

# Layer identifiers must match exactly for muting to work, so these examples
# use absolute paths throughout. asset_path() builds them from one place.
ASSETS = os.path.abspath("_assets")
os.makedirs(ASSETS, exist_ok=True)

def asset_path(name):
    return os.path.join(ASSETS, name)

# Clear any layers left behind by a previous run before calling CreateNew.
for _name in ("root.usda", "shot.usda", "base.usda"):
    _stale = Sdf.Layer.Find(asset_path(_name))
    if _stale:
        _stale.Clear()
    if os.path.exists(asset_path(_name)):
        os.remove(asset_path(_name))
```

### Example 1: Directing Edits Into a Specific Layer

We build a small layer stack with two {term}`sublayers <Sublayer>`: `base.usda` holding the published value, and `shot.usda` holding a stronger shot-level override. Notice that the root layer ends up empty, because every edit was directed somewhere else.

```{code-cell}
:test-tags: [edit-targets-author]
:emphasize-lines: 15-21

from pxr import Usd, UsdGeom, Sdf

base = Sdf.Layer.CreateNew(asset_path("base.usda"))
shot = Sdf.Layer.CreateNew(asset_path("shot.usda"))
root = Sdf.Layer.CreateNew(asset_path("root.usda"))

# Sublayers are listed strongest first
root.subLayerPaths = ["./shot.usda", "./base.usda"]
stage: Usd.Stage = Usd.Stage.Open(root)

# The stage starts out targeting its root layer
print("Edit target is the root layer:", stage.GetEditTarget().GetLayer() == root)

# Author the published value into the weaker base layer
with Usd.EditContext(stage, base):
    ball: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/World/Ball")
    ball.GetRadiusAttr().Set(1.0)

# Author a shot-level override into the stronger shot layer
with Usd.EditContext(stage, shot):
    ball.GetRadiusAttr().Set(5.0)

print("Composed radius:", ball.GetRadiusAttr().Get())
print("base.usda holds:", base.GetAttributeAtPath("/World/Ball.radius").default)
print("shot.usda holds:", shot.GetAttributeAtPath("/World/Ball.radius").default)
print("root.usda is empty:", root.GetPrimAtPath("/World") is None)

root.Save(); base.Save(); shot.Save()
```

The composed radius is `5.0` because `shot.usda` is the stronger sublayer. Both opinions still exist, each in the layer we targeted. Looking at all three layers makes the split concrete.

`root.usda` holds nothing but the sublayer list, even though it was the stage's original edit target. Every edit was redirected elsewhere:

```{code-cell}
:tags: [remove-input]
DisplayCode(asset_path("root.usda"))
```

`base.usda` holds the full prim definition, because `UsdGeom.Sphere.Define()` ran while this layer was targeted:

```{code-cell}
:tags: [remove-input]
DisplayCode(asset_path("base.usda"))
```

`shot.usda` holds an `over` rather than a `def`. The prim already existed from `base.usda`, so targeting `shot.usda` authored an override of the radius instead of a second definition. The edit target decides which layer receives an opinion; OpenUSD still decides what kind of spec is needed to express it:

```{code-cell}
:tags: [remove-input]
DisplayCode(asset_path("shot.usda"))
```

### Example 2: Muting a Layer to Isolate a Contribution

Now we mute the shot layer. The stage falls back to the base value, but nothing is edited or lost.

```{code-cell}
:test-tags: [edit-targets-muting]
:emphasize-lines: 11-12

import os

from pxr import Usd, UsdGeom, Sdf

root = Sdf.Layer.FindOrOpen(asset_path("root.usda"))
shot = Sdf.Layer.FindOrOpen(asset_path("shot.usda"))
stage: Usd.Stage = Usd.Stage.Open(root)
ball: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Ball")

print("Before muting:", ball.GetRadiusAttr().Get())

stage.MuteLayer(shot.identifier)

print("After muting: ", ball.GetRadiusAttr().Get())
print("Muted layers: ", [os.path.basename(p) for p in stage.GetMutedLayers()])
print()
print("The layer still holds its opinion:", shot.GetAttributeAtPath("/World/Ball.radius").default)
print("Muting written into the root layer?", "mute" in root.ExportToString().lower())

stage.UnmuteLayer(shot.identifier)
print("After unmuting:", ball.GetRadiusAttr().Get())
```

This is the bisecting workflow in miniature: mute a layer, see whether the problem disappears, and you have found which layer is responsible. Because muting is not scene description, you can do this on production files without any risk of committing the change.

### Example 3: Muting Is Per-Stage

To show that muting really is stage-local, we mute a layer on one stage and then open a second stage on the same root layer.

```{code-cell}
:test-tags: [edit-targets-per-stage]
:emphasize-lines: 10-12

from pxr import Usd, UsdGeom, Sdf

root = Sdf.Layer.FindOrOpen(asset_path("root.usda"))
shot = Sdf.Layer.FindOrOpen(asset_path("shot.usda"))

stage_a: Usd.Stage = Usd.Stage.Open(root)
stage_a.MuteLayer(shot.identifier)

# A completely separate stage opened on the same root layer
stage_b: Usd.Stage = Usd.Stage.Open(root)

print("stage_a sees the layer muted:", stage_a.IsLayerMuted(shot.identifier))
print("stage_b sees the layer muted:", stage_b.IsLayerMuted(shot.identifier))
print()
print("stage_a radius:", UsdGeom.Sphere.Get(stage_a, "/World/Ball").GetRadiusAttr().Get())
print("stage_b radius:", UsdGeom.Sphere.Get(stage_b, "/World/Ball").GetRadiusAttr().Get())

stage_a.UnmuteLayer(shot.identifier)
```

Two stages built from identical scene description disagree about what the composed radius is, purely because one of them has a layer muted. That is the clearest demonstration that muting lives on the stage rather than in the data.

```{seealso}
The {term}`session layer <Session Layer>` is the other half of this picture. It is a scratch layer at the top of the root layer stack that makes a natural edit target for temporary, application-level overrides, and `Usd.Stage.Save()` deliberately does not write it to disk.
```

## Key Takeaways

Edit targets control where authored opinions are written, and layer muting controls which layers are read. Neither changes the structure of your layer stack, which is what makes both safe to use on production scenes.

Use {usdcpp}`UsdEditContext` rather than `SetEditTarget` so the previous target is always restored, and remember that targeting a weak layer still produces a weak opinion. Use muting for temporary, exploratory work: it is stage-level state that is never saved, never shared between stages, and never recorded in scene description. When toggling several layers, batch the changes through `MuteAndUnmuteLayers` so composition is only rebuilt once.
