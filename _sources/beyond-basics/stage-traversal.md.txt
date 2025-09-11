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

kernelspec:
  name: python3
  display_name: python3
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.13'
    jupytext_version: 1.17.2
---

# Stage Traversal

## What Is Stage Traversal?

Stage traversal is the process of traversing the scenegraph of a stage with the purpose of querying or editing the scene data. We can traverse the scenegraph by iterating through child prims, accessing parent prims, and traversing the hierarchy to find specific prims of interest.

```{kaltura} 1_ott9hzic
```

### How Does It Work?

Traversing stages works via the `Usd.PrimRange` iterator. Other methods like `Usd.Stage.Traverse` return a `Usd.PrimRange` iterator. The difference is that `Usd.PrimRange` takes a starting prim as an argument and `Usd.Stage.Traverse` starts it's traversal from the stage's pseudo-root.

Traversals operate by walking prim by prim in depth-first order. You can use predicates and `Usd.PrimRange.PruneChildren` to optimize your traversals if you know you don't need to visit certain branches.

There are two traversal modes:

* **Default**: Iterate over child prims
* **PreAndPostVisit**: Iterate over the hierarchy and visit each prim twice, once when first encountering it, and then again when "exiting" the child hierarchy.

There are also predicates which can be used for pre-filtering the result:

* `Usd.PrimIsActive` 
  * If the active metadata is `True`
  * Analogous to `Usd.Prim.IsActive()`
* `Usd.PrimIsLoaded`
  * If the (ancestor) payload is loaded
  * Analogous to `Usd.Prim.IsLoaded()`
* `Usd.PrimIsModel`
  * If the kind is a sub kind of `Kind.Tokens.model`
  * Analogous to `Usd.Prim.IsModel()`
* `Usd.PrimIsGroup`
  * If the kind is `Kind.Tokens.group`
  * Analogous to `Usd.Prim.IsGroup()`
* `Usd.PrimIsAbstract`
  * If the prim specifier is `Sdf.SpecifierClass`
  * Analogous to `Usd.Prim.IsAbstract()`
* `Usd.PrimIsDefined`
  * If the prim specifier is `Sdf.SpecifierDef`
  * Analogous to `Usd.Prim.IsDefined()`


### Working With Python


```python
# This yields all active, loaded, defined, non-abstract prims on this stage depth-first
Usd.Stage.Traverse()

# Traverse all prims in the stage
Usd.Stage.TraverseAll()

# Predicates are combined used bitwise operators
predicate = Usd.PrimIsActive & Usd.PrimIsLoaded

# Traverse starting from the given prim and based on the predicate for filtering the traversal
Usd.PrimRange(prim, predicate=predicate)

# You must use iter() to invoke iterator methods like Usd.PrimRange.PruneChildren()
it = iter(Usd.PrimRange.Stage(stage))
for prim in it:
    if prim.GetName() == "Environment":
        prim_range.PruneChildren()  # Skip all children of "Environment"
```


## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook. It wil also create a stage used in the examples.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode


from pxr import Usd, UsdGeom, UsdLux, UsdShade

file_path = "_assets/stage_traversal.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# Define a new Scope primitive at the path "/World/Environment" on the current stage
env: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Environment"))

# Define a new DistantLight primitive at the path "/World/Environment/SkyLight" on the current stage
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, env.GetPath().AppendPath("SkyLight"))

stage.Save()
```

For reference, this the USDA for the stage that we will be using in the following examples:
```{code-cell}
:tags: [remove-input]
DisplayCode(file_path)
```

### Example 1: Traversing Through the Stage

To traverse through the stage, we can use the [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) method. This traversal will yield prims that are active, loaded, defined, non-abstract on the stage in depth-first order.

```{code-cell}
:emphasize-lines: 7-10

# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# Traverse and print the paths for the visited prims
for prim in stage.Traverse():
    # Print the path of each prim
    print(prim.GetPath())
```

Note how the prims were printed in depth-first order. All of the descendants of `/World/Box` appear before `/World/Environment` and its descendants.

### Example 2: Traversing USD Content for Specific Prim Types

For this practical example, we will traverse the stage to operate on specific prims based on their types.

We can filter based on the type of the prim. For example, we can check if the prim is of type `scope` or `xform`. To do this we pass the prim into the constructor method for the prim type we are interested in. For example,`UsdGeom.Scope(prim)` is equivalent to [`UsdGeom.Scope.Get(prim.GetStage(), prim.GetPath())`](https://openusd.org/release/api/class_usd_geom_scope.html#a538339c2aa462ebcf1eb07fed16f9be4) for a valid prim. If the prim's type does not match, it will return an invalid prim.

```{code-cell}
:emphasize-lines: 7-21

# Import necessary modules from the pxr package
from pxr import Usd, UsdGeom

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

scope_count = 0
xform_count = 0
# Traverse through each prim in the stage
for prim in stage.Traverse():
    # Check if the prim is of type Scope
    if UsdGeom.Scope(prim):
        scope_count += 1
        print("Scope Type: ", prim.GetName())
    # Check if the prim is of type Xform
    elif UsdGeom.Xform(prim):
        xform_count +=1
        print("Xform Type: ", prim.GetName())

print("Number of Scope prims: ", scope_count)
print("Number of Xform prims: ", xform_count)
```

### Example 3: Traversing Through the Children of a Prim

Using [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) can be a powerful tool, but for large stages, more efficient and targeted methods should be considered. A way to be more efficient and targeted is to traverse through the children of a prim.

If you need to work within a specific scope or hierarchy in the stage, you can perform a traversal starting from a particular prim. Let's take a look at how we can traverse through the children of the default prim.

```{code-cell}
:emphasize-lines: 10-13

# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Open the USD stage from the specified file:
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# Get the default prim of the stage (/World in this case):
default_prim: Usd.Prim = stage.GetDefaultPrim()

# Iterate through all children of the default prim
for child in default_prim.GetAllChildren():
    # Print the path of each child prim
    print(child.GetPath())
```


### Example 4: Traversing Using Usd.PrimRange

[`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) will return a [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) object. `UsdPrimRange` exposes pre- and post- prim visitations allowing for a more involved traversals. It can also be used to perform actions such as pruning subtrees.

Let's see an example of [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) in use.


```{code-cell}
:emphasize-lines: 7-9

# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

prim_range = Usd.PrimRange(stage.GetPrimAtPath("/World/Box"))
for prim in prim_range:
    print(prim.GetPath())
```

Note how only "/World/Box" and its descendants are printed.

There are other ways to use [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) such as passing in [`predicates`](https://openusd.org/release/api/prim_flags_8h.html#Usd_PrimFlags), you can find more information in the [Using Usd.PrimRange in Python](https://openusd.org/release/api/class_usd_prim_range.html#details) section of `UsdPrimRange`.


## Key Takeaways

Traversal is how we navigate the scenegraph and query scene data. Traversal can be made more efficient by limiting the number of prims it visits.
