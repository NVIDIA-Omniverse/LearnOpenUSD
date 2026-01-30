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

orphan: true
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

## What Is a Material?

### How Does It Work?

### Working With Python

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from lousd.utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: UsdShade and Material

[`UsdShade`](https://openusd.org/release/api/usd_shade_page_front.html) is a {term}`schema <Schema>` for creating and binding materials.

[`Material`](https://openusd.org/release/api/class_usd_shade_material.html) provides a container to store data for defining a "shading material" to a renderer.

`UsdShade` and `Materials` will be covered in later topics and are only covered here to show another use case for schema-specific APIs.

> **NOTE:** The material is not applied to the cube so it will not show up in the scene visually, but it is displayed in the hierarchy.

```{code-cell}

from pxr import Usd, UsdGeom, UsdShade

stage: Usd.Stage = Usd.Stage.CreateNew("_assets/materials.usda")

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
DisplayUSD("_assets/materials.usda", show_usd_code=True)
```


## Key Takeaways