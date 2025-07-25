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

## What are References?
This lesson talks briefly about references. The word may seem familiar – we introduced the concept in the previous lesson on composition and strength ordering, where "references" represents the R in LIVRPS.

A rerefence in Universal Scene Description is a composition arc that enables the composition of prims and their descendants onto other prims – this allows us to use references to aggregate larger scenes from smaller, modular units of scene description. This can be done with external references, which graft data from other files, or internal references, which graft data from other parts of the hierarchy.

They are fundamental in USD's composition system, enabling modular and reusable scene description, and they are the second most important composition arc in USD, after sublayers.

![](../images/References_Definition.webm)

### How Does It Work?

A reference arc includes the address of the layer to reference from (which can be omitted for internal references) and the prim path to reference (which can be omitted if you want to load an entire external layer which has a default prim defined).

When a prim is composed via a reference arc, USD first composes the layer stack of the referenced prim, then adds the resulting prim spec to the destination prim. Then, it applies any overrides or additional composition arcs from the destination prim.

### Working With Python

![References Python](../images/References_Python.webm)

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

### Example 1: Defining a Reference Prim

[References](https://openusd.org/release/glossary.html#usdglossary-references) are a [composition arc](https://openusd.org/release/glossary.html#usdglossary-compositionarcs). [References](https://openusd.org/release/glossary.html#usdglossary-references) are like links to separate pieces of a project, allowing you to include and reuse these pieces without copying them.

Here's an example of how a reference looks in `.usda`:

```python
#usda 1.0

def Xform "World"
{
    def Xform "Geometry"
    {
        def Xform "Box" (
            prepend references = @../resources/cubebox_a02_distilled/cubebox_a02_distilled.usd@
        )
        {
        }
    }
}
```

Firstly, we want to grab all references of a prim. To do this we use [`GetReferences()`](https://openusd.org/release/api/class_usd_prim.html#ac9081d27e9d2a1058e32249fb96aaa34). This returns a [`UsdReferences`](https://openusd.org/release/api/class_usd_references.html) object, which allows us to add, remove, and modify references.

To add a reference, we use [`AddReference()`](https://openusd.org/release/api/class_usd_references.html#a95bf456b23a234d3aa017015a4ad05e0). Let's see these in practice.

```{code-cell}
:emphasize-lines: 16-21

from pxr import Usd, UsdGeom, Gf

# Create a new stage and define a cube:
file_path = "assets/cube.usda"
stage = Usd.Stage.CreateNew(file_path)
cube = UsdGeom.Cube.Define(stage, "/Cube")
stage.SetDefaultPrim(cube.GetPrim())
stage.Save()

# Create a second file path and stage, define a world and a sphere:
second_file_path = "assets/shapes.usda"
stage = Usd.Stage.CreateNew(second_file_path)
world = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# Define a reference prim and set its translation:
reference_prim = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Cube_Ref")).GetPrim()
UsdGeom.XformCommonAPI(reference_prim).SetTranslate(Gf.Vec3d(5, 0, 0))

# Add a reference to the "cube.usda" file:
reference_prim.GetReferences().AddReference("./cube.usda")

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(second_file_path, show_usd_code=True)
```

Notice that the cube prim **DOES NOT** show up in the scene. 

The code is correct, but the composed result is not what we wanted because of a local opinion in our current layer stack. The local opinion in `shapes.usda` is stating that "Cube_Ref" is an Xform and that trumps the opinion from `cube.usda` where we defined a Cube. Thus, the render is correct because the composed result for "Cube_Ref" is that it is an Xform, not a Cube prim. In the next part we will go over how we can adjust this using an Xform to wrap around the cube.

+++ {"tags": ["remove-cell"]}
>**NOTE**: Run the cell below to clear cleanup Example 1 before Example 2.
+++
```{code-cell}
:tags: [remove-input]
import os
os.remove("assets/cube.usda")
os.remove("assets/shapes.usda")
stage = None
```

### Example 2: Understanding How LIVRPS Affects References

In the example above, you noticed that the cube prim defined in `cube.usda` was not showing up after we referenced it in `shapes.usda`. As we mentioned before, [references](https://openusd.org/release/glossary.html#usdglossary-references) are a [composition arc](https://openusd.org/release/glossary.html#usdglossary-compositionarcs).

In the current layer stack, we have a local opinion that ranks higher than our reference. `Xform` in `shapes.usda` is our local opinion which out weighs our reference `Cube` in `cube.usda`. 

One way to solve this is wrapping the Cube prim in an Xform. Below is the code change we would have to make.



```{code-cell} 
from pxr import Usd, UsdGeom, Gf

# Create a new stage 
file_path = "assets/cube.usda"
stage = Usd.Stage.CreateNew(file_path)

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Define the world Xform:
world = UsdGeom.Xform.Define(stage, "/World")

# Define a cube and set it as the default prim:
cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Cube"))
stage.SetDefaultPrim(world.GetPrim())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


# Save the stage
stage.Save()


# Create a new stage and define the world xform
second_file_path = "assets/shapes.usda"
stage = Usd.Stage.CreateNew(second_file_path)
world = UsdGeom.Xform.Define(stage, "/World")

# Define a sphere and set its parent to the world xform
UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# Define a reference prim and set its translation
reference_prim = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Cube_Ref")).GetPrim()
UsdGeom.XformCommonAPI(reference_prim).SetTranslate(Gf.Vec3d(5, 0, 0))

# Add a reference to the :cube.usda: file
reference_prim.GetReferences().AddReference("./cube.usda")

# Save the stage
stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(second_file_path, show_usd_code=True)
```


### Example 3: Adding References and Adding Attributes

[References](https://openusd.org/release/glossary.html#usdglossary-reference) in OpenUSD allow for the inclusion of external assets or sub-scene data into a scene. This mechanism helps in modularizing and reusing assets across different scenes and projects, enabling efficient management of large-scale 3D environments.

Here, we'll add a reference as an example for creating attributes in USD.

```{code-cell}

from pxr import Usd, UsdGeom

file_path = "assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a root Xform named "World"
world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Define a child Xform named "Geometry" under the "World" Xform
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

# Define a new Xform named "Box" under the root "Geometry" Xform
box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()

# Add a reference to a USD file containing a box geometry
box_prim.GetReferences().AddReference("box/cubebox_a02_distilled/cubebox_a02_distilled.usd")

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


# Get the property names of the box primitive
box_prop_names = box_prim.GetPropertyNames()

# Print each property name
for prop_name in box_prop_names:
    print(prop_name)

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD("assets/custom_attributes.usda", show_usd_code=True)
```


The [`UsdGeomXformOp`](https://openusd.org/release/api/class_usd_geom_xform_op.html) is a schema wrapper for `UsdAttribute`. 

We will see in the next cell how we can create attributes using `CreateAttribute()`.

Generally, we always should check if the attribute exists first before. The schema methods are clearer and easier to use.

```{code-cell}

from pxr import Usd, UsdGeom

file_path = "assets/custom_attributes2.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)


world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("box/cubebox_a02_distilled/cubebox_a02_distilled.usd")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Get the children of the box prim
box_prim_children = box_prim.GetChildren()
box_inst_children = box_prim_children[0].GetChildren()

# Create a Xform object from the second child of the box prim
box_xform: UsdGeom.Xform = UsdGeom.Xform(box_inst_children[2].GetChildren()[0])

# Add/Get Scale Op
if box_xform.GetScaleOp():
    box_scale_attr = box_xform.GetScaleOp()
else:
    box_scale_attr = box_xform.AddScaleOp()

# Set Scale Op
box_scale_attr.Set((2.0, 1.0, 1.0))

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

## Key Takeaways

So, why is it important to understand and leverage references properly? References have several practical use cases. As mentioned earlier, references are useful for building large, complex scenes by referencing smaller sub-scenes or components. We see referencing used commonly for asset libraries, where you might have assets, materials or other props reused across several scenes.

By leveraging references, artists and developers can create more efficient workflows, manage complex scenes, and collaborate more effectively across different departments and production stages.

