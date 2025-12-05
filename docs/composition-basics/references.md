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
# Referencing Basics

## What Are References?
This lesson talks briefly about {term}`references <Reference>`. The word may seem familiar – we introduced the concept in the previous lesson on {term}`composition <Composition>` and {term}`strength ordering <LIVERPS Strength Ordering>`, where "references" represents the R in LIVRPS.

A reference in Universal Scene Description is a composition arc that enables the composition of {term}`prims <Prim>` and their descendants onto other prims – this allows us to use references to aggregate larger scenes from smaller, modular units of scene description. This can be done with external references, which graft data from other files, or internal references, which graft data from other parts of the hierarchy.

They are fundamental in USD's composition system, enabling modular and reusable scene description, and they are the second most important composition arc in USD, after {term}`sublayers <Sublayer>`.

![](../images/foundations/References_Definition.webm)

### How Does It Work?

A reference arc includes the identifier of or path to the {term}`layer <Layer>` to reference from (which can be omitted for internal references) and the prim {term}`path <Path>` to reference (which can be omitted if you want to load an entire external layer which has a default prim defined).

When a prim is composed via a reference arc, USD first composes the {term}`layer stack <Layer Stack>` of the referenced prim, then adds the resulting {term}`prim spec <Prim Spec>` to the destination prim. Then, it applies any overrides or additional {term}`composition arcs <Composition Arcs>` from the destination prim.

### Working With Python

Here are a few ways you can work with references using the Python API:

```python
# Return a UsdReferences object for managing references on a prim
prim.GetReferences()

# Add a reference to the specified asset and prim path
references.AddReference(assetPath, primPath) 

# Remove all references from a prim
references.ClearReferences()
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Adding a Reference

References are a composition arc. References are like links to separate pieces of a project, allowing you to include and reuse these pieces without copying them.

Here's an example of how a reference looks in `.usda`:

```python
#usda 1.0

def Xform "World"
{
    def Xform "Geometry"
    {
        def Xform "Box" (
            prepend references = @./cubebox_a02/cubebox_a02.usd@
        )
        {
        }
    }
}
```

Firstly, we want to grab all references of a prim. To do this we use [`GetReferences()`](https://openusd.org/release/api/class_usd_prim.html#ac9081d27e9d2a1058e32249fb96aaa34). This returns a [`UsdReferences`](https://openusd.org/release/api/class_usd_references.html) object, which allows us to add, remove, and modify references.

To add a reference, we use [`AddReference()`](https://openusd.org/release/api/class_usd_references.html#a95bf456b23a234d3aa017015a4ad05e0). Let's see these in practice.

```{code-cell}
:emphasize-lines: 16-22

from pxr import Usd, UsdGeom, Gf

# Create a new stage and define a cube:
file_path = "_assets/cube.usda"
stage = Usd.Stage.CreateNew(file_path)
cube = UsdGeom.Cube.Define(stage, "/Cube")
stage.SetDefaultPrim(cube.GetPrim())
stage.Save()

# Create a second file path and stage, define a world and a sphere:
second_file_path = "_assets/shapes.usda"
stage = Usd.Stage.CreateNew(second_file_path)
world = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# Define a reference prim and set its translation:
reference_prim = stage.DefinePrim(world.GetPath().AppendPath("Cube_Ref"))

# Add a reference to the "cube.usda" file:
reference_prim.GetReferences().AddReference("./cube.usda")
# Position the cube
UsdGeom.XformCommonAPI(reference_prim).SetTranslate(Gf.Vec3d(5, 0, 0))

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(second_file_path, show_usd_code=True)
```

Here we created a {term}`stage <Stage>` representing a Cube prim and then used a reference arc to incorporate it into a new stage, `shapes.usda` that also defined a Sphere prim.


### Example 2: Referencing an External Asset

References in OpenUSD allow for the inclusion of external {term}`assets <Asset>` or sub-scene data into a scene. This mechanism helps in modularizing and reusing assets across different scenes and projects, enabling efficient management of large-scale 3D environments.

Here, we'll add a reference to a shipping box asset.

+++ {"tags": ["remove-cell"]}
>**NOTE**: Run the cell below copy the required asset to the right location for the example.
+++
```{code-cell}
:tags: [remove-input]
import shutil
# cleanup any existing copy
try:
    shutil.rmtree('_assets/cubebox_a02')
except FileNotFoundError:
    pass
shutil.copytree('../exercise_content/foundations/cubebox_a02', '_assets/cubebox_a02')
```

```{code-cell}
:emphasize-lines: 12-17

from pxr import Usd, UsdGeom

file_path = "_assets/asset_ref.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a root Xform named "World"
world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a child Xform named "Geometry" under the "World" Xform
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

# Define a new Xform named "Box" under the root "Geometry" Xform
box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()

# Add a reference to a USD file containing a box geometry
box_prim.GetReferences().AddReference("./cubebox_a02/cubebox_a02.usd")

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD("_assets/asset_ref.usda", show_usd_code=True)
```


## Key Takeaways

So, why is it important to understand and leverage references properly? References have several practical use cases. As mentioned earlier, references are useful for building large, complex scenes by referencing smaller sub-scenes or components. We see referencing used commonly for asset libraries, where you might have assets, materials or other props reused across several scenes.

By leveraging references, artists and developers can create more efficient workflows, manage complex scenes, and collaborate more effectively across different departments and production stages.

