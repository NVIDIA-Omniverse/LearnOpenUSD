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

# Relationships

## What Is a Relationship?
{term}`Relationships <Relationship>` establish connections between {term}`prims <Prim>`, acting as pointers or links between objects in the scene hierarchy. A relationship allows a prim to target or refer to other prims, {term}`attributes <Attribute>`, or even other relationships. This establishes dependencies between scenegraph objects.

### How Does It Work?

Relationships store {term}`path <Path>` values that point to other scene elements. When you query a relationship's targets, OpenUSD performs {term}`path translations <Path Translation>` to map the authored target paths to the corresponding objects in the composed scene
prims.

Relationships are robust against path translations, a key advantage over hard-coded paths. If a target prim's path changes due to editing or referencing, the relationship automatically remaps to the new location.

Relationships can have multiple targets, making them useful for grouping or collecting objects together. For example, a material relationship might target all geometry prims that should use that material.

Note that a relationship is an alternative type of {term}`property <Property>` to an attribute. Unlike an attribute, it has no data type. It is a way of declaring, at creation time, that the only use for a property is to record linkage
information. Conceptually, it is like an attribute whose data type is a "link". This means you can _not_ use a relationship to connect two already-existing attributes--for that, you can use {term}`attribute connections <Connection>`.

### Working With Python

Here are a few Python commands to familiarize yourself as you work with relationships. These can be useful as you establish connections between different scene elements, like materials and geometry.

```python
# Get the target paths of a relationship
UsdRelationship.GetTargets()

# Set the target paths for a relationship
UsdRelationship.SetTargets()

# Add a new target path to a relationship
UsdRelationship.AddTarget()

# Remove a target path from a relationship
UsdRelationship.RemoveTarget()
```
## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
from utils.helperfunctions import create_new_stage
```

### Example 1: Prim Collections with Relationships
Relationships are properties that store one or more target paths. You can author a relationship with `CreateRelationship`, then later retrieve it with `GetRelationship` and inspect the targets with `GetTargets`.
```{code-cell}
:emphasize-lines: 15-25

from pxr import Usd, UsdGeom, Gf

file_path = "_assets/relationships_ex1.usda"
stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a sphere under the World Xform:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))

# Define a cube under the World Xform and set it to be 5 units away from the sphere:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Create typeless container for the group
group = stage.DefinePrim("/World/Group") 

# Define the relationship
group.CreateRelationship("members", custom=True).SetTargets(
    [sphere.GetPath(), cube.GetPath()]
)

# List relationship targets
members_rel = group.GetRelationship("members")
print("Group members:", [str(p) for p in members_rel.GetTargets()])

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

### Example 2: Using a Built‑in Relationship (proxyPrim)
Many built‑in schemas expose `Relationships`. `UsdGeom.Imageable` has `proxyPrim`, which points a high cost prim to a lightweight proxy.
```{code-cell}
:emphasize-lines: 14-22

from pxr import Usd, UsdGeom

file_path = "_assets/relationships_ex2.usda"
stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a "high cost" Sphere Prim under the World Xform:
high: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("HiRes"))

# Define a "low cost" Cube Prim under World Xfrom
low: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Proxy"))

UsdGeom.Imageable(high).GetPurposeAttr().Set("render")
UsdGeom.Imageable(low).GetPurposeAttr().Set("proxy")

# Author the proxy link on the render Prim
UsdGeom.Imageable(high).GetProxyPrimRel().SetTargets([low.GetPath()])

# Tools that honor proxyPrim should draw the proxy in preview
draw_prim = UsdGeom.Imageable(high).ComputeProxyPrim()  # returns Usd.Prim
print("Preview should draw:", str(draw_prim[0].GetPath() if draw_prim else high.GetPath()))

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

### Example 3: Material Binding Relationships
Material binding is encoded as a relationship named `material:binding` that targets a `UsdShade.Material`. The `UsdShade.MaterialBindingAPI` authors and reads this relationship. Here GreenMat is bound to two cubes and RedMat is bound to one cube.
```{code-cell}
:emphasize-lines: 15-40

from pxr import Usd, UsdGeom, UsdShade, Gf, Sdf

file_path = "_assets/relationships_ex3.usda"
stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")


cube_1: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube_1"))
cube_2: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube_2"))
UsdGeom.XformCommonAPI(cube_2).SetTranslate(Gf.Vec3d(5, 0, 0))
cube_3: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube_3"))
UsdGeom.XformCommonAPI(cube_3).SetTranslate(Gf.Vec3d(10, 0, 0))

# Create typeless container for the materials
looks = stage.DefinePrim("/World/Looks")

# Create simple green material for preview
green: UsdShade.Material = UsdShade.Material.Define(stage, looks.GetPath().AppendPath("GreenMat"))
green_ps = UsdShade.Shader.Define(stage, green.GetPath().AppendPath("PreviewSurface"))
green_ps.CreateIdAttr("UsdPreviewSurface")
green_ps.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.0, 1.0, 0.0))
green.CreateSurfaceOutput().ConnectToSource(green_ps.ConnectableAPI(), "surface")

# Create simple red material for preview
red: UsdShade.Material = UsdShade.Material.Define(stage, looks.GetPath().AppendPath("RedMat"))
red_ps = UsdShade.Shader.Define(stage, red.GetPath().AppendPath("PreviewSurface"))
red_ps.CreateIdAttr("UsdPreviewSurface")
red_ps.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 0.0, 0.0))
red.CreateSurfaceOutput().ConnectToSource(red_ps.ConnectableAPI(), "surface")

# Bind materials to Prims
UsdShade.MaterialBindingAPI.Apply(cube_1.GetPrim()).Bind(green)
UsdShade.MaterialBindingAPI.Apply(cube_2.GetPrim()).Bind(green)
UsdShade.MaterialBindingAPI.Apply(cube_3.GetPrim()).Bind(red)

# Verify by reading the direct binding
for prim in [cube_1, cube_2, cube_3]:
    mat = UsdShade.MaterialBindingAPI(prim).GetDirectBinding().GetMaterial()
    print(f"{prim.GetPath()} -> {mat.GetPath() if mat else 'None'}")

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

## Key Takeaways

Relationships enable robust encoding of dependencies and associations between scene elements, such as:

* Binding geometry to materials
* Grouping prims into collections
* Establishing connections in shading networks
* Associating scene elements with non-hierarchical links (e.g. material binding)

Using relationships instead of hard paths enhances:

* Non-destructive editing workflows
* Referencing and asset reuse across tools
* Collaborative workflows across teams

Relationships are a way to link scene elements while enabling non-destructive editing and cross-tool collaboration. They enhance the flexibility and scalability of OpenUSD-based pipelines.



