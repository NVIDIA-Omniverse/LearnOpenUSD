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
# Scope 

Understanding Scopes is important as they help in organizing and managing complexity in large-scale 3D scenes.

## What Is a Scope?

In OpenUSD, a Scope is a special type of {term}`prim <Prim>` that is used primarily as a grouping mechanism in the scenegraph. It does not represent any geometry or renderable content itself but acts as a container for organizing other prims. Think of Scope as an empty folder on your computer where you organize files; similarly, Scope helps in structuring and organizing prims within a USD scene.

```{kaltura} 1_ybhfy6qq
```

### How Does It Work?

Scope prims are used to create a logical grouping of related prims, which can be particularly useful in complex scenes with numerous elements. For example, a Scope might be used to group all prims related to materials, animation, or geometry. A key feature of Scopes is that they cannot be transformed, which promotes their usage as lightweight organizational containers. All transformable child prims (such as geometry prims or Xforms) will be evaluated correctly from within the Scope prim and down the hierarchy. This organization aids in simplifying scene management, making it easier for teams to navigate, modify, and render scenes.

### Working With Python

When working with Scope in USD using Python, a couple functions are particularly useful:

```python
# Used to define a new Scope at a specified path on a given stage
UsdGeom.Scope.Define(stage, path)

# This command is generic, but it's useful to confirm that a prim's type is a Scope, ensuring correct usage in scripts
prim.IsA(UsdGeom.Scope)
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Define a Scope
[`Scope`](https://openusd.org/release/api/class_usd_geom_scope.html) is a grouping primitive and does NOT have transformability. It can be used to organize libraries with large numbers of entry points. It also is best to group actors and environments under partitioning Scopes. Besides navigating, it's easy for a user to {term}`deactivate <Active and Inactive>` all actors or environments by deactivating the root scope.

We can define `Scope`using [`UsdGeom.Scope.Define()`](https://openusd.org/release/api/class_usd_geom_scope.html#acdb17fed396719a9a21294ebca0116ae).

```{code-cell}
:emphasize-lines: 12-28

from pxr import Usd, UsdGeom, Gf

file_path = "_assets/scope.usda"
stage = Usd.Stage.CreateNew(file_path)

# World container (transformable)
world = UsdGeom.Xform.Define(stage, "/World")

num_a_prims = 2
num_b_prims = 2

# Two organizational Scopes (non-transformable grouping prims)
a_scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("A_Scope"))
b_scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("B_Scope"))

# Populate the scopes with some geometry
for a in range(num_a_prims):
    sphere = UsdGeom.Sphere.Define(stage, a_scope.GetPath().AppendPath(f"A_Sphere_{a}"))
    UsdGeom.XformCommonAPI(sphere).SetTranslate(Gf.Vec3d(a*2.5, 0, 0))

for b in range(num_b_prims):
    cube = UsdGeom.Cube.Define(stage, b_scope.GetPath().AppendPath(f"B_Cube_{b}"))
    UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(b*2.5, -2.5, 0))

# Deactivate the A_Scope
a_scope.GetPrim().SetActive(False)

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```
For more information on active vs. inactive prims see {doc}`../beyond-basics/active-inactive-prims` lesson.


## Key Takeaways

Scope prims in OpenUSD play a crucial role in the organization and management of complex 3D scenes. Its primary function is to serve as a container for other prims, helping maintain clarity and structure in large projects.

