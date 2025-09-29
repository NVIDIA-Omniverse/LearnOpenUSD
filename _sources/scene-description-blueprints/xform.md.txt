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
# Xform

In Universal Scene Description, Xforms play a key role in defining the spatial transformations of objects in a scene.

## What Is an Xform?
In OpenUSD, an Xform is a type of prim that stores transformation data, such as translation, rotation, and scaling, which apply to its child prims. This makes Xforms a powerful tool for grouping and manipulating the spatial arrangement of objects in a 3D scene. Xform stands for 'transform', reflecting its role in transforming the space in which its children reside.

```{kaltura} 1_1bbmv128
```

### How Does It Work?

Xform prims allow for hierarchical transformations, meaning that
transformations applied to a parent Xform affect all of its child prims. This is essential in complex scenes where multiple objects need to move or scale relative to the parent. Typical use cases include animating characters or robotic arms, where different parts are children of an Xform prim, or arranging furniture in architectural visualization, where all items in a room might be scaled or rotated together.

### Working With Python

Working with Xform in USD via Python involves several functions:

```python
# Used to define a new Xform prim at a specified path on a given stage
UsdGeom.Xform.Define(stage, path)

# Retrieves the order of transformation operations, which is crucial for understanding how multiple transformations are combined. Different orders can yield different results, so understanding XformOpOrder is important. 
xform.GetXformOpOrderAttr()
	
# Adds a new transform operation to the Xform prim, such as translation or rotation, with specified value   
xform.AddXformOp(opType, value)
```

## Examples

### Example 1: UsdGeom and Xform

[`UsdGeom`](https://openusd.org/release/api/usd_geom_page_front.html) defines the 3D graphics-related prim and property schemas that together form a basis for interchanging geometry between Digital Content Creation (DCC) tools in a graphics pipeline.

Some things to know about `UsdGeom`:

- All classes in `UsdGeom` inherit from [`UsdGeomImageable`](https://openusd.org/release/api/class_usd_geom_imageable.html), whose intent is to capture any prim type that might want to be rendered or visualized.
- All geometry prims are directly transformable. [`UsdGeomXformable`](https://openusd.org/release/api/class_usd_geom_xformable.html) encapsulates the schema for a prim that is transformable.  

[`UsdGeomXform`](https://openusd.org/release/api/class_usd_geom_xform.html) is a concrete prim schema for a transform, which is transformable and can transform other child prims as a group.


```{code-cell}
:emphasize-lines: 7-8

# Import the necessary modules from the pxr package:
from pxr import Usd, UsdGeom

# Create a new USD stage with root layer named "xform_prim.usda":
file_path = "_assets/xform_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a new Xform primitive at the path "/World" on the current stage:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Save changes to the current stage to its root layer:
stage.Save()
print(stage.ExportToString(addSourceFileComment=False))
```

## Key Takeaways

Now, we've explored what Xform prims are and how they function within the USD framework. We've seen how Xform prims are essential for defining and managing spatial transformations in a scene, making them indispensable for any 3D content creation workflow.



