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

# Model Kinds

In this lesson, we'll explore the concept of {term}`kinds <Kind>` in OpenUSD.

## What Are Model Kinds?
![Kind Definition](../images/foundations/Kind_Definition.webm)

Model kinds are prim‑level metadata that classify a prim’s role in the model hierarchy. They are tokens from the Kind registry that tools use to create a standardized, queryable structure, independent of the prim’s schema type. Kind is not another prim type (like `UsdGeomScope` or `UsdGeomXform`); it is metadata that other tools and pipelines can rely on. With kinds authored, you can target only models using `UsdPrim` helpers like `IsModel`, `IsGroup`, `IsComponent`, and `IsSubComponent`, and you can traverse models with predicates such as `UsdPrimIsModel`. As a rule of thumb, groups and assemblies organize models, components are leaf models, and subcomponents mark important interior nodes.

Understanding kinds enables the creation of modular, reusable assets, and employing them effectively can have a significant impact on how well we can manage complex 3D scenes.


### How Does It Work?

Kinds are a set of predefined categories that define the role and behavior of different prims within the scene hierarchy. These kinds include group, assembly, component, and subcomponent.

{term}`Group <Group>`, {term}`assembly <Assembly>`, {term}`component <Component>` all inherit from the base kind "model", which is why we refer to these as model kinds. {term}`Subcomponent <Subcomponent>` is the outlier. "Model" is an abstract kind and should not be assigned as any {term}`prim <Prim>`. This is what the inheritance structure looks like:

* model
  * component
  * group
    * assembly
* subcomponent

Kinds are extensible so you can add new taxonomies, but at the cost of content portability. Consumers need to know what your custom taxonomies mean and how to reason about them. Refer to the {usdcpp}`kind documentation <kind_page_front>` for more information about extending kinds.

![Kind Components](../images/foundations/Kind_Component.webm)

![A diagram depicting a house icon and a pen icon.](../images/foundations/Artboard_27_1.png)

#### Component

Let's start with component. A component is a reusable, self-contained asset that is complete and referenceable. "Component" is a relatively familiar word, so it’s helpful to think of component models as a consumer-facing product like a pen or a house. While drastically different in scale, both would be logical component models in a hierarchy.

#### Subcomponent

A component cannot contain other component models as descendants, which is why
we have subcomponents. Subcomponents aren't model kinds, but they are a way to identify that some prim within a component might be important.


![a diagram representing a neighborhood](../images/foundations/Artboard_28_1.png)

#### Groups and Assemblies

Zooming back out to the bigger picture, all parents of a component model must
have their kind metadata set to "group" or "assembly". A group is an
organizational unit within a model, used to logically group related models
together. Similarly, an assembly, which is a subkind of group, serves as a
container for combining various parts or assets into a larger, more complex
entity. In the example of the house as our component, the neighborhood or city
might be assembly models. The assembly model may contain multiple group
scopes, such as trees and street lights in the neighborhood.


![Diagram showing model hierarchy of the neighborhood example](../images/foundations/Artboard_47.png)

#### Model Hierarchy

Prims of the group, assembly, and component kind (and any custom kind
inheriting from them) make up the {term}`model hierarchy <Model Hierarchy>`. This hierarchy is designed so that we can better organize assets in our scene. It facilitates navigation, asset management, and high-level reasoning about the scene structure.

We can leverage model hierarchy to prune traversal in the scenegraph. For
example, all ancestral prims of component models (when they’re correctly
grouped) are part of the model hierarchy, while all descendants are not.


### Working With Python

![Kind Python](../images/foundations/Kind_Python.webm)

There are a few ways you can interact with model kinds using Python.

```python

from pxr import Usd, Kind

# Construct a Usd.ModelAPI on a prim
prim_model_api = Usd.ModelAPI(prim)

# Return the kind of a prim
prim_model_api.GetKind()

# Set the kind of a prim to component
prim_model_api.SetKind(Kind.Tokens.component) 

# Return "true" if the prim represents a model based on its kind metadata
prim.IsModel()  
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

### Example 1: Traversal with Model Kinds

This example shows the practical benefit of Model Kinds.  `/World` is marked as a group so children can qualify as models, `/World/Component` is classified as a component, and `/World/Markers` is left untagged. Model‑only traversal allow for edits only to the component while the markers remain untouched.

```{code-cell}
:emphasize-lines: 9-40
from pxr import Usd, UsdGeom, Kind, Gf

# Create stage and model root
file_path = "_assets/model_kinds_component.usda"
stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())

# Make /World a group so children can be models
Usd.ModelAPI(world_xform.GetPrim()).SetKind(Kind.Tokens.group)

# Non-model branch: Markers (utility geometry, no kind)
markers = UsdGeom.Scope.Define(stage, world_xform.GetPath().AppendChild("Markers"))

points = {
    "PointA": Gf.Vec3d(-3, 0, -3), "PointB": Gf.Vec3d(-3, 0, 3),
    "PointC": Gf.Vec3d(3, 0, -3), "PointD": Gf.Vec3d(3, 0, 3)
    }
for name, pos in points.items():
    cone = UsdGeom.Cone.Define(stage, markers.GetPath().AppendChild(name))
	cone.CreateAxisAttr(UsdGeom.Tokens.y)
    UsdGeom.XformCommonAPI(cone).SetTranslate(pos)
    cone.CreateDisplayColorPrimvar().Set([Gf.Vec3f(1.0, 0.85, 0.2)])

# Model branch: a Component we want to place as a unit
component = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendChild("Component"))
Usd.ModelAPI(component.GetPrim()).SetKind(Kind.Tokens.component)
body = UsdGeom.Cube.Define(stage, component.GetPath().AppendChild("Body"))
body.CreateDisplayColorPrimvar().Set([(0.25, 0.55, 0.85)])
UsdGeom.XformCommonAPI(body).SetScale((3.0, 1.0, 3.0))

# Model-only traversal: affect models, ignore markers
for prim in Usd.PrimRange(stage.GetPseudoRoot(), predicate=Usd.PrimIsModel):
    if prim.IsComponent():
        xformable = UsdGeom.Xformable(prim)
        if xformable:
            UsdGeom.XformCommonAPI(xformable).SetTranslate((0.0, 2.0, 0.0))

# Show which prims were considered models
model_paths = [p.GetPath().pathString for p in Usd.PrimRange(stage.GetPseudoRoot(), predicate=Usd.PrimIsModel)]
print("Model prims seen by traversal:", model_paths)

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

## Key Takeaways

Model kinds in OpenUSD provide a structured way to organize and manage complex 3D scenes. By defining and adhering to these kinds, artists, designers, and developers can create modular, reusable assets that can be easily combined, referenced, and shared across different projects and workflows.
