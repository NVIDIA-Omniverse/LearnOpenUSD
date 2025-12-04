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
# XformCommonAPI

## What Is XformCommonAPI?
`XformCommonAPI ` is a non-applied {term}`API schema <API Schema>` of the OpenUSD framework. Today, we're diving into this API to understand its utility in the 3D content creation pipeline.

This API facilitates the authoring and retrieval of a common set of operations with a single translation, rotation, scale and pivot that is generally compatible with import and export into many tools. It's designed to simplify the interchange of these transformations.

```{kaltura} 1_tx9y8k5c
```

### How Does It Work?

The API provides methods to get and set these transformations at specific times--for instance, it allows the retrieval of transformation vectors at any
given frame or {term}`time code <Time Code>`, ensuring precise control over the simulation process.

There’s another way to author and retrieve translations – through the `UsdGeomXformable` function. Xformable {term}`prims <Prim>` support arbitrary sequences of transformations, which gives power users a lot of flexibility. A user could place two rotations on a "Planet" prim, allowing them to control revolution and rotation around two different pivots on the same prim. This is powerful, but complicates simple queries like "What is the position of an object at time 101.0?"

### Working With Python

This example verifies prim compatibility with `XformCommonAPI` and demonstrates its use.

``` python 
from pxr import Usd, UsdGeom

# Create a stage and define a prim path
stage = Usd.Stage.CreateNew('example.usda')
prim = UsdGeom.Xform.Define(stage, '/ExamplePrim')

# Check if the XformCommonAPI is compatible with the prim using the bool operator 
if not (xform_api := UsdGeom.XformCommonAPI(prim)):
    raise Exception("Prim not compatible with XformCommonAPI")

# Set transformations
xform_api.SetTranslate((10.0, 20.0, 30.0))
xform_api.SetRotate((45.0, 0.0, 90.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)
xform_api.SetScale((2.0, 2.0, 2.0))
```

These functions demonstrate how to apply translations, rotations, and scaling to a 3D object using the `XformCommonAPI`. We can get a transformation matrix
from the xformable prim that works with any `xformOp` order using the [`GetLocalTransformation`](https://openusd.org/release/api/class_usd_geom_xformable.html#a9a04ccb1ba8aa16e8cc1e878c2c92969) method.

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: XformCommonAPI - Transforms and Inheritance

In this example, we will use the [`XformCommonAPI`](https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html) to translate, rotate, and scale a parent Xform, then show how a child under that parent inherits those transforms while a similar child under a separate {term}`prim hierarchy <Namespace>` does not.

```{code-cell}
:emphasize-lines: 10-34

from pxr import Usd, UsdGeom, Gf

file_path = "_assets/xformcommonapi.usda"
stage = Usd.Stage.CreateNew(file_path)

# A root transform group we will move and rotate
world = UsdGeom.Xform.Define(stage, "/World")
parent = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Parent_Prim"))

# Parent Translate, Rotate, Scale using XformCommonAPI
parent_xform_api = UsdGeom.XformCommonAPI(parent)
parent_xform_api.SetTranslate(Gf.Vec3d(5, 0, 3))
parent_xform_api.SetRotate(Gf.Vec3f(90, 0, 0))
parent_xform_api.SetScale(Gf.Vec3f(3.0, 3.0, 3.0))


child_translation = Gf.Vec3d(2, 0, 0)

# Child A - inherits parent transforms
child_a_cone = UsdGeom.Cone.Define(stage, parent.GetPath().AppendChild("Child_A"))
child_a_xform_api = UsdGeom.XformCommonAPI(child_a_cone)
child_a_xform_api.SetTranslate(child_translation)  # Parent_Prim transform + local placement

# Child B - "/World/Alt_Parent/Child_B" does NOT inherit Parent_Prim transforms
alt_parent = UsdGeom.Xform.Define(stage, world.GetPath().AppendChild("Alt_Parent"))
child_b_cone = UsdGeom.Cone.Define(stage, alt_parent.GetPath().AppendChild("Child_B"))
child_b_xform_api = UsdGeom.XformCommonAPI(child_b_cone)
child_b_xform_api.SetTranslate(child_translation)  # local placement only

# Inspect the authored Xform Operation Order
print("Parent xformOpOrder:", UsdGeom.Xformable(parent).GetXformOpOrderAttr().Get())
print("Alt_Parent xformOpOrder:", UsdGeom.Xformable(alt_parent).GetXformOpOrderAttr().Get())
print("Child A xformOpOrder:", UsdGeom.Xformable(child_a_cone).GetXformOpOrderAttr().Get())
print("Child B xformOpOrder:", UsdGeom.Xformable(child_b_cone).GetXformOpOrderAttr().Get())

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

`XformCommonAPI` is used to set and get transform components such as scale, rotation, scale-rotate pivot and translation. Even though these are considered {term}`attributes <Attribute>`, it is best to go through `XformCommonAPI` when editting transformation values. `XformCommonAPI` is a great way to bootstrap setting up new transformations. Future modules will dive into advanced usage of xformOps. 


## Key Takeaways

The `XformCommonAPI` provides the preferred way for authoring and retrieving a standard set of component transformations including scale, rotation, scale-
rotate pivot and translation.

The goal of the API is to enhance, reconfigure or adapt each structure without changing the entire system. This approach allows for flexibility and customization by focusing on the individual parts rather than the whole. This is done by limiting the set of allowed basic operations and by specifying the order in which they are applied.
