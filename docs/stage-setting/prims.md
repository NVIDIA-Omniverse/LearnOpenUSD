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
# Prims

Welcome to this lesson on OpenUSD {term}`prims <Prim>`. In this lesson, we will:

* Identify the role of prims, including what a prim is and its role within a OpenUSD {term}`stage <Stage>`.

## What Is a Prim?

Primitives, or prims for short, are the building blocks of any OpenUSD scene, making understanding them essential for anyone working with 3D content creation and manipulation in the OpenUSD ecosystem.

```{kaltura} 1_trdtyb7a
```

A prim is the core component within the USD framework. Think of a prim as a container that holds various types of data, {term}`attributes <Attribute>`, and {term}`relationships <Relationship>` which define an object or entity within a scene. A prim can be a type of visual or non-visual entity, such as a mesh, a material, or a light or an xform. Prims are organized in a hierarchical structure, creating a scenegraph that represents the relationships and transformations between objects in the scene.

Each prim has a unique identifier known as a {term}`path <Path>`, which helps in locating it within the scenegraph. For example, a prim’s path might be `/World/BuildingA/Geometry/building_geo`, indicating that it is a child of the `Geometry` prim, which itself is a child of the `BuildingA` prim, and so on.

### How Does It Work?

Prims can have various types of attributes associated with them, such as position, rotation, scale, material information, animation data, and more. These properties define the attributes and relationships of the objects they represent.

A key feature of USD prims is their ability to encapsulate data, allowing them to be shared, referenced, and instanced across different scenes and files. Typical use cases include defining {term}`models <Model>`, cameras, lights, or even groups of other prims. The ability to efficiently manage and manipulate these prims non-destructively is what makes USD so powerful in various industries where complex scenes are the norm.


### Working With Python

In Python, working with prims involves several methods using the USD Python
API:

```python
# Generic USD API command. Used to define a new prim on a stage at a specified path, and optionally the type of prim.
stage.DefinePrim(path, prim_type)

# Specific to UsdGeom schema. Used to define a new prim on a USD stage at a specified path of type Xform. 
UsdGeom.Xform.Define(stage, path)
	
# Retrieves the children of a prim. Useful for navigating through the scenegraph.
prim.GetChildren()
	
# Returns the type of the prim, helping identify what kind of data the prim contains.
prim.GetTypeName()

# Returns all properties of the prim.
prim.GetProperties()
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

### Example 1: Defining a Prim

A prim is the primary container object in USD. It can contain other prims and properties holding data.

To create a generic prim on the stage we use [`DefinePrim()`](https://openusd.org/release/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730). By default, the prim will be typeless meaning that it's just an empty container. By introducing a prim type, we can begin to dictate what kind of data the prim contains depending on if it is a prim to represent a cube, a light, a mesh, etc.

```{code-cell}
:emphasize-lines: 7-11

# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Create a new USD stage with root layer named "prims.usda":
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/prims.usda")

# Define a new primitive at the path "/hello" on the current stage:
stage.DefinePrim("/hello")

# Define a new primitive at the path "/world" on the current stage with the prim type, Sphere.
stage.DefinePrim("/world", "Sphere")

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD("_assets/prims.usda", show_usd_code=True)
```

Note in the USDA output that the prim with the name "hello" does not have a type, but the prim named "world" has the type, Sphere.

### Example 2: Defining a Sphere Prim

While the [`DefinePrim()`](https://openusd.org/release/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) API provides a generic way to create any type of prim. Many prim types have specific API to create and interact with them.


```{code-cell}
:emphasize-lines: 6-8

from pxr import Usd, UsdGeom

file_path = "_assets/sphere_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a prim of type `Sphere` at path `/hello`:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/hello")
sphere.CreateRadiusAttr().Set(2)

# Save the stage:
stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

In this example, we used the `UsdGeom.Sphere` class to create a Sphere type prim and set some data about that sphere. We set there sphere's `radius` to `2`. Using the `UsdGeom.Sphere` class provides a more transparent interface for the Sphere prim type.

### Example 3: Creating a Prim Hierarchy

Prims can contain other prims to create a {external+usd:ref}`namespace hierarchy <glossary:Namespace>`.

```{code-cell}
:emphasize-lines: 6-11

from pxr import Usd, UsdGeom

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a Scope prim in stage at `/Geometry`
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
# Define an Xform prim in the stage as a child of /Geometry called GroupTransform
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath("GroupTransform"))
# Define a Cube in the stage as a child of /Geometry/GroupTransform, called Box
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath("Box"))

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

The prim hierarchy that we have created is:

- *Geometry*
    - *GroupTransform*
        - *Cube*

By nesting prims in this way, a hierarchical scenegraph begins to take shape. In this example, "Geometry" is the root prim. In other words, "Geometry" is a direct child of the pseudo-root `/`. We are also defining three different types of prims here: [`Scope`](https://openusd.org/release/api/class_usd_geom_scope.html), [`Xform`](https://openusd.org/release/api/class_usd_geom_xform.html), and [`Cube`](https://openusd.org/release/api/class_usd_geom_cube.html). We will look at these prim types more closely in other lessons, but for a brief description:

- **Xform**: Defines a transform (translate, rotation, scale)
- **Scope**: Is a simple container that does not hold transform data
- **Cube**: Defines a primitive rectilinear cube

### Example 4: Does the Prim Exist?

When working with large amounts of data it is key to make sure that a prim exists before trying to override it. We can get the child of a prim using [`GetChild()`](https://openusd.org/release/api/class_usd_prim.html#a8c0974bbd49570564f0096ce982ff64a). If it was unable to find the child, it will return an invalid `UsdPrim`. An invalid prim will evaluate as `False` when treated as a boolean. You can use [`Usd.Object.IsValid()`](https://openusd.org/release/api/class_usd_object.html#ac532c4b500b1a85ea22217f2c65a70ed) to check if the prim is valid or exists. 

```{code-cell}
:emphasize-lines: 6-11

from pxr import Usd

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")
child_prim: Usd.Prim
if child_prim := prim.GetChild("Box"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")
```
Here is the USDA output of `_assets/prim_hierarchy.usda` to verify.
```{code-cell}
:tags: [remove-input]
DisplayCode(file_path)
```
`Box` is not a child of `Geometry`. If we change `Box` to `GroupTransform` then it will print out "Child prim exists". That is because `GetChild()` only returns the direct child of the prim, not nested children.

```{code-cell}
:emphasize-lines: 8-8

from pxr import Usd

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")
child_prim: Usd.Prim
if child_prim := prim.GetChild("GroupTransform"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")
```
Here is the USDA output of `_assets/prim_hierarchy.usda` to verify.
```{code-cell}
:tags: [remove-input]
DisplayCode(file_path)
```

## Key Takeaways

In this lesson, we covered what a prim is in the context of OpenUSD, its characteristics, and its role in building and managing 3D scenes. We also looked at how prims facilitate data encapsulation and sharing, which are critical for complex 3D project workflows. Understanding prims is foundational as we start working with OpenUSD.
