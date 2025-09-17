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
# Active and Inactive Prims

## What Are Active and Inactive Prims?

![](../images/foundations/ActiveInactive_Definition.webm)

In OpenUSD, all prims are active by default. Making a prim inactive is effectively a non-destructive deletion of a prim from a stage. Deactivating a prim provides a way to temporarily remove, or prune, prims and their descendants from being composed and processed on the stage, which can make traversals more efficient.

An active prim and its active child prims will be visited and processed during stage traversals and operations. However, by making a prim inactive by setting its "active" metadata to _false_, we prevent that prim itself from being visited. This also prevents its descendant prims from being composed onto the stage.

```python
# Make the prim at /Parent inactive
stage.GetPrimAtPath('/Parent').SetActive(False)
```

Deactivating a prim is a non-destructive operation–-the prim still exists in the scene description, but it is pruned from the composed stage view until reactivated. This is effectively the way to delete a prim from the stage.

### How Does It Work?

Deactivation is useful for managing scene complexity and scalability by pruning unnecessary scene data. It provides a way to non-destructively remove parts of the scene graph without permanently deleting them.

When a prim is deactivated, it has the following effects:

* The prim itself will be excluded from default [stage traversals](./stage-traversal.md) as determined by the `UsdPrimDefaultPredicate`.
* All scene description for the deactivated prim's descendants will not be composed onto the stage.

However, the inactive state can be overridden by stronger layer opinions that set the "active" metadata to _true_ for that prim. This allows selective reactivation of pruned subtrees.

![ActiveInactivePython](../images/foundations/ActiveInactive_Python.webm)

### Working With Python

We can use the following Python functions to set the "active" metadata on a prim and check to see if the prim is currently active on the stage.

* `UsdPrim.SetActive(bool)` - Set the "active" metadata for a prim
* `UsdPrim.IsActive()` - Return whether a prim is currently active on the stage

## Examples

### Example 1: Setting Prims as Active/Inactive

+++ {"tags": ["remove-cell"]}
>**NOTE**: The next cell is content setup for this example..
+++
```{code-cell}
:tags: [remove-input]

from pxr import Usd, UsdGeom, UsdLux, UsdShade

stage: Usd.Stage = Usd.Stage.CreateNew("_assets/active-inactive.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# Define a new Scope primitive at the path "/World/Environment" on the current stage
env: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Environment"))

# Define a new DistantLight primitive at the path "/World/Environment/SkyLight" on the current stage
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, env.GetPath().AppendPath("SkyLight"))

stage.Save()
```

[Active/Inactive](<inv:usd:std#glossary:active / inactive>) prim is a behavior that is non-destructive and provides reversible prim deletion from a stage. By default, all prims are active. Active prims are visited by [stage traversals](./stage-traversal.md). If a prim is inactive that means it is not visited by stage traversals, and neither will its child prims.

{usdcpp}`UsdPrim::SetActive` is used to set whether the prim is active or inactive. Giving the value of `False` will make it inactive and `True` to make it active.

In this example, we will print out the contents of a stage at the start and then see how the contents change after deactivating a prim. Here's is what the USDA for this stage looks like:

```{code-cell}
:emphasize-lines: 15-16

from pxr import Usd

# Open the USD stage from the specified file
file_path = "_assets/active-inactive.usda"
stage = Usd.Stage.Open(file_path)

# Iterate through all the prims on the stage
# Print the state of the stage before deactivation
print("Stage contents BEFORE deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())

# Get the "/World/Box" prim and deactivate it
box = stage.GetPrimAtPath("/World/Box")
# Passing in False to SetActive() will set the prim as Inactive and passing in True will set the prim as active
box.SetActive(False)

print("\n\nStage contents AFTER deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())
```

You can see that the `/World/Box` prim and all of its descendant prims have be excluded on the second traversal because we deactivated `/World/Box`.

## Key Takeaways

![](../images/foundations/ActiveInactive_Inactive.webm)

The active/inactive behavior in OpenUSD allows for non-destructive pruning of scene data from the composed stage view. Deactivating prims helps manage scene complexity by temporarily removing unnecessary scene elements, while still
preserving the ability to reactivate them later. This pruning mechanism is an important tool for optimizing performance and managing large, complex USD scenes in production pipelines.



