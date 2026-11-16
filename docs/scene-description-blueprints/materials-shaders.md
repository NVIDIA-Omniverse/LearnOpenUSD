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
# Materials and Shaders

In this lesson, we'll explore materials and shaders in OpenUSD, {term}`schemas <Schema>` belonging to the `UsdShade` domain. Understanding them lets you describe how a surface looks once, in the scene itself, so that every application reading the scene can render it the same way.

## What Is a Material?

A material describes how a surface responds to light: its color, how rough or glossy it is, whether it is metallic. In OpenUSD, a material is a {term}`prim <Prim>` of type `Material`. It does not hold those values itself. It is a container for a *shading network*, a set of connected shader prims whose combined result the material presents to a renderer.

`UsdShade` provides the pieces of that network:

* Materials (`UsdShadeMaterial`), the container that a renderer looks up and that geometry is bound to
* Shaders (`UsdShadeShader`), the nodes of the network, each naming an implementation and exposing inputs and outputs
* Node graphs (`UsdShadeNodeGraph`), which group shaders behind their own inputs and outputs so a sub-network can be reused
* Material binding (`UsdShadeMaterialBindingAPI`), the {term}`API schema <API Schema>` that assigns a material to geometry

### How Does It Work?

A shader prim names its implementation with its `info:id` {term}`attribute <Attribute>`. The most widely supported is `UsdPreviewSurface`, a small surface shader defined in the [UsdPreviewSurface Specification](inv:usd:std:doc#spec_usdpreviewsurface) so that content can look consistent across applications. A shader's parameters are attributes in the `inputs:` namespace, such as `inputs:diffuseColor`, and its results are attributes in the `outputs:` namespace.

Shaders are wired together by *connections*. A connection is authored on an input or output and points at the source that supplies its value. The network ends at the material's terminal outputs, such as `outputs:surface` for how the surface responds to light and `outputs:displacement` for how it is displaced. A material can carry terminals for more than one shading system, for example `outputs:mdl:surface` alongside `outputs:surface`, so one material can serve renderers that use different shading languages.

Geometry receives a material through a *binding*: a `material:binding` {term}`relationship <Relationship>` authored on the geometry prim and targeting the material. Bindings are inherited down the {term}`namespace <Namespace>` hierarchy. A binding on a parent prim applies to every descendant that has no binding of its own, so one binding can dress a whole assembly while individual parts override it.

### Working With Python

Here are a few relevant Python commands for working with materials and shaders:

```python
# Import the UsdShade module
from pxr import Sdf, UsdShade

# Define a material, and a shader inside it
material = UsdShade.Material.Define(stage, "/World/Looks/Mat")
shader = UsdShade.Shader.Define(stage, "/World/Looks/Mat/PreviewSurface")

# Name the shader's implementation and set one of its inputs
shader.CreateIdAttr("UsdPreviewSurface")
shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)

# Connect the material's surface terminal to the shader's surface output
material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

# Bind the material to a geometry prim
UsdShade.MaterialBindingAPI.Apply(geom_prim).Bind(material)
```

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
:test-tags: [materials-setup]
from lousd.utils.visualization import DisplayUSD, DisplayCode
from lousd.utils.helperfunctions import create_new_stage
```

### Example 1: Defining a Material

[`UsdShade`](https://openusd.org/release/api/usd_shade_page_front.html) is the schema domain for creating and binding materials.

{usdcpp}`UsdShadeMaterial` provides a container to store data for defining a "shading material" to a renderer. We'll start by defining one, inside a `Materials` scope that keeps it apart from the geometry it will dress.

```{code-cell}
:test-tags: [materials-usdshade-material]

from pxr import Usd, UsdGeom, UsdShade

stage: Usd.Stage = create_new_stage("_assets/materials.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Define a new Scope primitive at the path "/World/Box/Materials" on the current stage:
mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))

# Define a new Material primitive at the path "/World/Box/Materials/BoxMat" on the current stage:
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
```
```{note}
The material has no shading network yet and is not bound to the cube, so it has no visible effect. The USDA below shows where it sits in the hierarchy.
```
```{code-cell}
:tags: [remove-input]
DisplayCode("_assets/materials.usda")
```

### Example 2: Building a Shading Network and Binding It

An empty material changes nothing. To give the cube a look, we'll add a {usdcpp}`UsdShadeShader` inside the material, name `UsdPreviewSurface` as its implementation, set a few of its inputs, connect the material's surface terminal to it, and then bind the material to the cube.

```{code-cell}
:test-tags: [materials-preview-surface]
:emphasize-lines: 15-29
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

file_path = "_assets/materials_bound.usda"
stage: Usd.Stage = create_new_stage(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))
mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# Define a Shader prim inside the material and name its implementation:
shader: UsdShade.Shader = UsdShade.Shader.Define(stage, box_mat.GetPath().AppendPath("PreviewSurface"))
shader.CreateIdAttr("UsdPreviewSurface")

# Set the shader's inputs. Each one is authored as an attribute in the `inputs:` namespace:
shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.8, 0.1, 0.1))
shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

# Connect the material's surface terminal to the shader's surface output:
box_mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

# Apply MaterialBindingAPI to the cube, then bind the material to it:
binding_api: UsdShade.MaterialBindingAPI = UsdShade.MaterialBindingAPI.Apply(box_geo.GetPrim())
binding_api.Bind(box_mat)

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

Look at the cube in the generated USDA. Applying the API schema added `MaterialBindingAPI` to its `apiSchemas` metadata, and binding authored a `material:binding` relationship that targets `BoxMat`. In the material, `outputs:surface.connect` points at the shader's `outputs:surface`. That one connection is what makes the shader the material's surface.

```{tip}
Always apply `MaterialBindingAPI` before binding. OpenUSD still resolves a binding authored on a prim without it, but warns that the API schema is missing.
```

### Example 3: Inheriting Bindings Down the Hierarchy

Bindings are inherited by descendants. In this example, we'll bind a red material once on a shelf that holds three boxes, bind a blue material directly on one of the boxes, and then ask each box which material it resolves to.

```{code-cell}
:test-tags: [materials-binding-inheritance]
:emphasize-lines: 41-50
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

file_path = "_assets/material_binding_inheritance.usda"
stage: Usd.Stage = create_new_stage(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
looks_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Looks"))


def create_preview_material(stage: Usd.Stage, path: Sdf.Path, color: Gf.Vec3f) -> UsdShade.Material:
    """Define a material whose surface is a UsdPreviewSurface of a single color.

    Args:
        stage: The stage to define the material on.
        path: The path of the material prim.
        color: The diffuse color of the surface.

    Returns:
        The new material.
    """
    material: UsdShade.Material = UsdShade.Material.Define(stage, path)
    shader: UsdShade.Shader = UsdShade.Shader.Define(stage, path.AppendPath("PreviewSurface"))
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(color)
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    return material


red_mat: UsdShade.Material = create_preview_material(stage, looks_scope.GetPath().AppendPath("Red"), Gf.Vec3f(0.8, 0.1, 0.1))
blue_mat: UsdShade.Material = create_preview_material(stage, looks_scope.GetPath().AppendPath("Blue"), Gf.Vec3f(0.1, 0.2, 0.8))

# Define a shelf holding three boxes, spaced apart along the X axis:
shelf: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Shelf"))
boxes: list[UsdGeom.Cube] = []
for i in range(3):
    box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, shelf.GetPath().AppendPath(f"Box_{i}"))
    UsdGeom.XformCommonAPI(box).SetTranslate((i * 3.0, 0.0, 0.0))
    boxes.append(box)

# Bind the red material once, on the shelf:
UsdShade.MaterialBindingAPI.Apply(shelf.GetPrim()).Bind(red_mat)

# Bind the blue material directly on the last box:
UsdShade.MaterialBindingAPI.Apply(boxes[2].GetPrim()).Bind(blue_mat)

# Ask each box which material it resolves to, and which prim's binding supplied it:
for box in boxes:
    material, binding_rel = UsdShade.MaterialBindingAPI(box.GetPrim()).ComputeBoundMaterial()
    print(f"{box.GetPath()} -> {material.GetPath()} (bound on {binding_rel.GetPrim().GetPath()})")

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

`Box_0` and `Box_1` have no binding of their own, so they resolve to the red material bound on the shelf. `Box_2` has its own binding, and by default a prim's own binding wins over one inherited from an ancestor.

```{note}
An ancestor can reverse that default. Setting the strength of its binding to `strongerThanDescendants` with `SetMaterialBindingStrength()` makes the ancestor's binding win over its descendants' own bindings, which is useful when an assembly's look must not be overridden part by part.
```

## Key Takeaways

OpenUSD separates how a surface looks from the geometry that carries it. A material is a container for a network of shaders, wired together through their inputs and outputs and ending at terminal outputs that a renderer reads. Geometry receives a material through a binding, and bindings flow down the hierarchy, so one binding can dress an entire assembly while individual parts override it.

By building materials from `UsdPreviewSurface`, developers and 3D practitioners can carry a surface's look between applications with the scene itself, and add terminals for other shading systems, such as MDL or MaterialX, without giving that portability up.
