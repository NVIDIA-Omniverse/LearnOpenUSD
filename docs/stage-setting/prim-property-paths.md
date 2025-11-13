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

# Prim and Property Paths

## What Is a Path?
In OpenUSD, a path represents the location of a prim or property within a scenegraph. The string representation for a prim path consists of a sequence of prim names separated by forward slashes (`/`), similar to file paths in a directory structure. The stage pseudo-root, which serves as the starting point for the hierarchy, is represented by a forward slash (`/`).

For example, the path `/World/Geometry/Box` represents a prim named `Box` that is a child of a prim named `Geometry`, which is a child of the root prim named `World`.

### How Does It Work?

Paths in OpenUSD are handled through the `pxr.Sdf.Path` class to encode path data including prims, properties (both attributes and relationships), and variants.

Prims are indicated by a slash separator, which indicates the namespace Child (ex: `"/geo/box"`)

Period separators after an identifier is used to introduce a property (ex: `"/geo/box.weight"`)

Variants are indicated by curly brackets, like this: (ex. `"/geo/box{size=large}"`)

They are used to:

1. **Uniquely identify prims and properties**. Each prim and property in a scene has a unique path that distinguishes it from other prims and properties. 
2. **Navigate the scene hierarchy**. Paths allow you to traverse the scene hierarchy via the USD stage and access specific prims.
3. **Specify locations for authoring**. When creating or modifying prims, paths are used to specify where the prims should be placed in the hierarchy on the USD stage.
4. **Query and filter prims**. Paths can be used to filter and select specific prims based on their location in the hierarchy using `Sdf.PathExpression`.

### Working With Python

![Path Python](../images/foundations/Path_Python.webm)

Here are a few Python functions relevant to paths in OpenUSD.

```python
# Import the Sdf class
from pxr import Sdf

# Return the path of a Usd.Prim as an Sdf.Path object
Usd.Prim.GetPath()

# Retrieve a Usd.Prim at the specified path from the Stage
Usd.Stage.GetPrimAtPath()
```

## Examples

+++ {"tags": ["remove-cell"]}
> **NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
from utils.helperfunctions import create_new_stage
```

### Example 1: Getting, Validating, and Defining Prims at Path  

Each prim has a [path](https://openusd.org/release/glossary.html#usdglossary-path) to describe its location in [namespace](https://openusd.org/release/glossary.html#usdglossary-namespace).

For example, we defined a prim `hello` at path `/hello` and another prim `world` at path `/hello/world`.

We can retrieve prims using their path using [`GetPrimAtPath()`](https://openusd.org/release/api/class_usd_stage.html#a6ceb556070804b712c01a7968f925735). This will either return a valid or invalid prim. When using `GetPrimAtPath()` we should always check if the returned prim is valid before using it.

To check if a prim is valid we can use the [`IsValid()`](https://openusd.org/release/api/class_usd_object.html#ac532c4b500b1a85ea22217f2c65a70ed) method. Valid means that the prim exists in the stage. Invalid is when the prim does not exist in the stage or when the path is invalid.

```{note}
When using `GetPrimAtPath()`, it will return type `UsdPrim`. If our prim is of type `UsdGeom`, we will not be able to use `UsdGeom` API schema on it.
```

```{code-cell}
:emphasize-lines: 7-20

from pxr import Usd

stage: Usd.Stage = Usd.Stage.CreateNew("_assets/paths.usda")
stage.DefinePrim("/hello")
stage.DefinePrim("/hello/world")

# Get the primitive at the path "/hello" from the current stage
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")

# Get the primitive at the path "/hello/world" from the current stage
hello_world_prim: Usd.Prim = stage.GetPrimAtPath("/hello/world")

# Get the primitive at the path "/world" from the current stage
# Note: This will return an invalid prim because "/world" does not exist, but if changed to "/hello/world" it will return a valid prim
world_prim: Usd.Prim = stage.GetPrimAtPath("/world")

# Print whether the primitive is valid
print("Is /hello a valid prim? ", hello_prim.IsValid())
print("Is /hello/world a valid prim? ", hello_world_prim.IsValid())
print("Is /world a valid prim? ", world_prim.IsValid())

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayCode("_assets/paths.usda")
```

### Example 2: Build and navigate prim paths with Sdf.Path
Construct prim paths with AppendChild, then validate and navigate them with IsPrimPath and GetParentPath

```{code-cell}
:emphasize-lines: 5-26
from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("_assets/paths_build_and_nav.usda")

# Build prim paths via Sdf.Path
world_path = Sdf.Path("/World")
geometry_path = world_path.AppendChild("Geometry")  # /World/Geometry
sphere_path = geometry_path.AppendChild("Sphere")  # /World/Geometry/Sphere

looks_path = world_path.AppendChild("Looks")  # /World/Looks
material_path = looks_path.AppendChild("Material")  # /World/Looks/Material

# Define prims at those paths
stage.DefinePrim(world_path)
stage.DefinePrim(geometry_path)
UsdGeom.Sphere.Define(stage, sphere_path)
stage.DefinePrim(looks_path)
stage.DefinePrim(material_path)

# Path checks and basic navigation
print("sphere_path IsPrimPath:", sphere_path.IsPrimPath())
print("sphere_path parent:",    sphere_path.GetParentPath())
print("Geometry prim valid:",   stage.GetPrimAtPath(geometry_path).IsValid())
print("\nmaterial_path IsPrimPath:", material_path.IsPrimPath())
print("material_path parent:",    material_path.GetParentPath())
print("Looks prim valid:",   stage.GetPrimAtPath(looks_path).IsValid())

stage.Save()

```
```{code-cell}
:tags: [remove-input]
DisplayCode("_assets/paths_build_and_nav.usda")
```

### Example 3: Author an attribute and a relationship from property paths
A property path identifies a property location but does not create anything by itself. You use AppendProperty to build the path, then author the spec with CreateAttribute or CreateRelationship

```{code-cell}
:emphasize-lines: 8-38

from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("_assets/paths_property_authoring.usda")

# A prim to work with
sphere = UsdGeom.Sphere.Define(stage, "/World/Geom/Sphere")

# Create a property path for the attribute /World/Geom/Sphere.userProperties:tag
attr_property_path = sphere.GetPath().AppendProperty("userProperties:tag")

# Working with the property path for the attribute
owner_prim = stage.GetPrimAtPath(attr_property_path.GetPrimPath())
attr_name = stage.GetPropertyAtPath(attr_property_path).GetPath().name  # "userProperties:tag"
print(f"Attribute property '{attr_name}' has been defined on {owner_prim.GetPath()} after AppendProperty: {owner_prim.GetAttribute(attr_name).IsDefined()}")

# Define the attribute on the owner prim
attr = owner_prim.CreateAttribute(attr_name, Sdf.ValueTypeNames.String)
print(f"\nAttribute property '{attr_name}' has been defined on {owner_prim.GetPath()} after CreateAttribute: {owner_prim.GetAttribute(attr_name).IsDefined()}")

attr.Set("surveyed")
print(f"Attribute value after Set: {stage.GetAttributeAtPath(attr_property_path).Get()}")

# Create a relationship from a property path
marker = UsdGeom.Xform.Define(stage, "/World/Markers/MarkerA")
# Create a property path for the relationship
rel_property_path = sphere.GetPath().AppendProperty("my:ref")  # /World/Geom/Sphere.my:ref

# Working with the property path for the relationship
owner_prim = stage.GetPrimAtPath(rel_property_path.GetPrimPath())
rel_name = stage.GetPropertyAtPath(rel_property_path).GetPath().name  # "my:ref"
print(f"\nRelationship property '{rel_name}' has been defined on {owner_prim.GetPath()} after AppendProperty: {owner_prim.GetRelationship(rel_name).IsDefined()}")

# Define the relationship on the owner prim
rel = owner_prim.CreateRelationship(rel_name)
print(f"\nRelationship property '{rel_name}' has been defined on {owner_prim.GetPath()} after CreateRelationship: {owner_prim.GetRelationship(rel_name).IsDefined()}")

rel.AddTarget(marker.GetPath())
print(f"Relationship targets after AddTarget: {[str(p) for p in stage.GetRelationshipAtPath(rel_property_path).GetTargets()]}")

stage.Save()

```
```{code-cell}
:tags: [remove-input]
DisplayCode("_assets/paths_property_authoring.usda")
```

## Key Takeaways

Using `Sdf.Path` objects in OpenUSD provides a way to uniquely identify and locate objects (prims) within our scene hierarchy. We will use paths for authoring, querying, and navigating USD data effectively.



