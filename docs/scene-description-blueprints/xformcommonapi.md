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
`XformCommonAPI ` is a non-applied API schema of the OpenUSD framework. Today, we're diving into this API to understand its utility in the 3D content creation pipeline.

This API facilitates the authoring and retrieval of a common set of operations with a single translation, rotation, scale and pivot that is generally compatible with import and export into many tools. It's designed to simplify the interchange of these transformations.

```{kaltura} 1_tx9y8k5c
```

### How Does It Work?

The API provides methods to get and set these transformations at specific times--for instance, it allows the retrieval of transformation vectors at any
given frame or TimeCode, ensuring precise control over the simulation process.

There’s another way to author and retrieve translations – through the `UsdGeomXformable` function. Xformable prims support arbitrary sequences of transformations, which gives power users a lot of flexibility. A user could place two rotations on a "Planet" prim, allowing them to control revolution and rotation around two different pivots on the same prim. This is powerful, but complicates simple queries like "What is the position of an object at time 101.0?"

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

### Example 1: Setting a Cone on a Cube

In this example, we will use the [`XformCommonAPI`](https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html) and a combination of transformations to set a Cone on top of a Cube.

```{code-cell}
:emphasize-lines: 10-15

from pxr import Usd, UsdGeom

file_path = "_assets/xformcommonapi.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

cone: UsdGeom.Cone = UsdGeom.Cone.Define(stage, "/Cone")
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, "/Cube")

cone.GetDisplayColorAttr().Set([(1.0, 0.5, 0.25)])
# Create an API object for the prim we want to manipulate
cone_xform_api = UsdGeom.XformCommonAPI(cone)
# Scale the cone to half its original size about the center of the cone.
cone_xform_api.SetScale((0.5, 0.5, 0.5))
# Move the cone up 1.5 meters: (half the cube's size + half the scaled cone's height) = (1.0 + 0.5)
cone_xform_api.SetTranslate((0.0, 1.5, 0.0))

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

`XformCommonAPI` is used to set and get transform components such as scale, rotation, scale-rotate pivot and translation. Even though these are considered attributes, it is best to go through `XformCommonAPI` when editting transformation values. `XformCommonAPI` is a great way to bootstrap setting up new transformations. Future modules will dive into advanced usage of xformOps. 


## Key Takeaways

The `XformCommonAPI` provides the preferred way for authoring and retrieving a standard set of component transformations including scale, rotation, scale-
rotate pivot and translation.

The goal of the API is to enhance, reconfigure or adapt each structure without changing the entire system. This approach allows for flexibility and customization by focusing on the individual parts rather than the whole. This is done by limiting the set of allowed basic operations and by specifying the order in which they are applied.
