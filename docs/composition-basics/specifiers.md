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

# Specifiers

## What Are Specifiers?

{term}`Specifiers <Specifier>` in OpenUSD convey the intent for how a {term}`prim <Prim>` or a {term}`prim spec <Prim Spec>` should be interpreted in the composed scene. The specifier can be one of three values: `def`, `over` or `class`.

### How Does It Work?

![Specifier Def](../images/foundations/Specifiers_Def.webm)

`def`, which is short for _{term}`define <Def>`_ , defines the prim in the current {term}`layer <Layer>`. `def` indicates a prim exists and concretely defined on the {term}`stage <Stage>`.

The resolved specifier of a prim--essentially, which specifier wins when the {term}`composition <Composition>` is completed--determines which stage traversals (like rendering) will visit that prim. Default traversals will only visit defined (`def`), non-abstract prims. Abstract prims are those that resolve to the `class` specifiers. `over`, the weakest specifier, will resolve to either a `def` or `class` specifier.

![Specifier Over](../images/foundations/Specifiers_Over.webm)

`over`, which is short for _{term}`override <Over>`_ , holds overrides for {term}`opinions <Opinions>` that already exist in the composed scene on another layer. The `over` will not translate back to the original prim, and is what enables non-destructive editing workflows, such as changing a {term}`property <Property>` of a prim, like its color, in another layer.  

![Specifier Class](../images/foundations/Specifiers_Class.webm)

A `class` prim essentially signals that it is a blueprint. `class` prims abstract and contain opinions that are meant to be composed onto other prims. It’s worth noting that `class` prims are intended as the target of a {term}`reference <Reference>`, {term}`payload <Payload>`, {term}`inherit <Inherit>`, or {term}`specialize <Specialize>` {term}`composition arc <Composition Arcs>` or as a {term}`relationship <Relationship>` target for a PointInstancer. These are concepts we'll cover in a later lesson.

Prims that resolve to `class` specifiers will also be present and composed on a stage, but won’t be visited by default stage traversals, meaning it will be ignored by traversals such as those used for rendering.

### Working With Python

![Specifier Python](../images/foundations/Specifiers_Python.webm)

Below is an example of how we can get or set a prim's specifier using Python.

```python
# Get a prim’s specifier
prim.GetSpecifier()

# Set a prim’s specifier
prim.SetSpecifier(specifier)
```

It's helpful to look at USDA files to understand how USD encodes specifiers in a USD layer. In this example, we're defining a new prim called "Box" with the type Cube and a `size` property set to `4`. The `def` specifier indicates that box is being concretely defined on the stage. 
```usda
def Cube "Box" {
    double size = 4
}
```

The `over` specifier sparsely modifies the `size` property without defining anything else about the prim; in this case, `size` is overriden to have a value of `10`. With an override like this, we may be trusting that the box has been defined in another layer, for example.

```usda
over "Box" {
    double size = 10
}
```
Lastly, we're authoring a new prim as a `class` called `"_box"`. This can be used as a reusable template in the USD scene.
```usda
class "_box" {
    double size = 4
}
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Authoring defs and a class in a base layer
This script defines two concrete cubes (specifier **def**) and a reusable **{term}`class <Class>`** prim that holds a `displayColor` opinion for inheritance. The output contrasts the composed specifiers for each, showing **def** for scene geometry and **class** for abstract Prim.

```{code-cell}
:emphasize-lines: 8-27
from pxr import Usd, UsdGeom, Sdf, Gf

base_file_path = "_assets/specifiers_base.usda"

stage = Usd.Stage.CreateNew(base_file_path)

# Create a simple scene with two cubes
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box_prim_cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendChild("Box"))
box_prim_cube.GetSizeAttr().Set(2.0)

box_2_prim_cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendChild("Box_2"))
box_2_prim_cube.GetSizeAttr().Set(2.0)
box_2_api = UsdGeom.XformCommonAPI(box_2_prim_cube)
box_2_api.SetTranslate(Gf.Vec3d(5, 0, 0))

# Define a class prim with a displayColor primvar
class_prim = stage.CreateClassPrim(world.GetPath().AppendPath("_Look/_green"))
class_prim_primvar_api = UsdGeom.PrimvarsAPI(class_prim)
class_prim_primvar_api.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray).Set([Gf.Vec3f(0.1, 0.8, 0.2)])

# Inspect specifiers
print("box specifier:", box_prim_cube.GetPrim().GetSpecifier())  # Sdf.SpecifierDef
print("box_2 specifier:", box_2_prim_cube.GetPrim().GetSpecifier())  # Sdf.SpecifierDef
print("class_prim specifier:", class_prim.GetSpecifier())  # e.g. Sdf.SpecifierClass

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(base_file_path, show_usd_code=True)
```


### Example 2: Non‑destructive over edits and class inherit
This script sublayers the base file, authors an {term}`over <Over>` on `/World/Box` to change `size`, and adds an **inherits** arc so the box picks up the class color. The prim‑stack printout makes it clear that the strong layer contributes over while the base contributes def, and the class opinions are applied via the inherit.

```{code-cell}
:emphasize-lines: 13-25
from pxr import Usd, UsdGeom, Sdf

new_file_path = "_assets/specifiers_over_base.usda"
base_file_path = "specifiers_base.usda"  # path relative to the new file

stage = Usd.Stage.CreateNew(new_file_path)

# Base is weaker than the root layer (root opinions are strongest)
stage.GetRootLayer().subLayerPaths = [base_file_path]

prim_path = "/World/Box"

# Author an override for the same prim
stage.OverridePrim(prim_path)

# Get the cube and change its size
box_prim_cube = UsdGeom.Cube.Get(stage, prim_path)
box_prim_cube.GetSizeAttr().Set(4.0)

# Compose the class onto the box using an inherit arc
box_prim_cube.GetPrim().GetInherits().AddInherit(Sdf.Path("/World/_Look/_green"))

# SdfPrimSpec handles, ordered strong to weak
for prim_spec in box_prim_cube.GetPrim().GetPrimStack():
    print(" - layer:", prim_spec.layer.identifier.split('/')[-1], "specifier:", prim_spec.specifier)

stage.Save()

```
```{code-cell}
:tags: [remove-input]
DisplayUSD(new_file_path, show_usd_code=True)
```


## Key Takeaways

Again, every prim will have a specifier. To have a prim present on the stage and available for processing you would define (`def`) that prim. You can use override specifiers, (`over`), to hold opinions that will be applied to prims defined in another layer and leverage non-destructive editing workflows, while class specifiers (`class`) can be leveraged to set up a set of opinions and properties to be composed by other prims.



