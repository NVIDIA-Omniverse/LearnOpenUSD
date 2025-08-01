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


## What is Stage Traversal?

Stage traversal is the process of traversing the scenegraph of a stage with the purpose of querying or editing the scene data. We can traverse the scenegraph by iterating through child prims, accessing parent prims, and traversing the hierarchy to find specific prims of interest.

Traversing stages works via the `Usd.PrimRange` class. Other methods like `stage.Traverse` use `Usd.PrimRange` as a base class.

Let’s review the Python functions we learned in the previous course that are relevant to traversal:

```python
# Open a USD file and create a Stage object
stage = Usd.Stage.Open('car.usda') 

# Traverses the stage of prims that are active
stage.Traverse() 

# Define a predicate to filter prims that are active and loaded
predicate = Usd.PrimIsActive & Usd.PrimIsLoaded

# Traverse starting from the given prim and based on the predicate for filtering the traversal
Usd.PrimRange(prim, predicate=predicate)
```

This module focuses on improving efficiency by limiting the number of prims that the process visits while traversing the stage.

### How Does It Work?

As a first step toward optimizing the traversal process, we can filter it based on the type of the prim, such as Scope or Xform. This enables us to be more efficient and targeted when we take the next step of traversing through the children of a prim.

`Usd.PrimRange` is another traversal method that, unlike `Traverse()`, can traverse through a pseudo root prim.

### Working With Python

For filtering prims during traversal, some Python functions are particularly useful:

```python
# Check whether the prim is of type Scope
if UsdGeom.Scope(prim)

# Get a specific child prim named "Environment" under the default prim
default_prim.GetChild("Environment")
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Setup

**Run the cell below to create the file that will be used for this lesson:**

```{code-cell}

from pxr import Usd, UsdGeom, UsdLux, UsdShade

file_path = "assets/tons_of_prims.usda"
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
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

### Example 1: Traversing Through the Stage

To traverse through the stage, we can use the [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) method. This traversal will yield prims from the current stage in depth-first-traversal order.

```{code-cell} ipython3
:cell_id: b3b417950ea74c6887cc1a6f89a0e64f
:deepnote_cell_type: code
:id: aZTCOSmnNOC_

# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("assets/tons_of_prims.usda")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Traverse through each prim (primitive) in the stage
for prim in stage.Traverse():
    # Print the path of each prim
    print(prim.GetPath())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
```

### Example 2: Traversing USD Content for Specific Prim Types

Using [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) can get costly as the stage scales.

We can filter based on the type of the prim. For example, we can check if the prim is of type `scope` or `xform`. To do this we pass the prim into the constructor method for the prim type we are interested in. For example,`UsdGeom.Scope(prim)` is equivalent to [`UsdGeom.Scope.Get(prim.GetStage(), prim.GetPath())`](https://openusd.org/release/api/class_usd_geom_scope.html#a538339c2aa462ebcf1eb07fed16f9be4) for a valid prim. If the prim's type does not match, it will return an invalid prim.

**Add the following code to the cell below, then run the cell:**

```python

```

```{code-cell}

# Import necessary modules from the pxr package
from pxr import Usd, UsdGeom

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("assets/tons_of_prims.usda")


# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Traverse through each prim (primitive) in the stage
for prim in stage.Traverse():
    # Check if the prim is of type Scope
    print(UsdGeom.Scope(prim))
    if UsdGeom.Scope(prim):
        print("Scope Type: ", prim.GetName())
    # Check if the prim is of type Xform
    elif UsdGeom.Xform(prim):
        print("Xform Type: ", prim.GetName())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
```

### Example 3: Traversing Through the Children of a Prim

Another way to be more efficient and targeted is to traverse through the children of a prim.

If you need to work within a specific scope or hierarchy in the stage, you can perform a traversal starting from a particular prim. Below shows a simple example on how to do this.

```python
from pxr import Usd

stage = Usd.Stage.Open('path/to/your.usda')
root_prim = stage.GetPrimAtPath("/root/path")

for prim in root_prim.GetChildren():
    # Perform operations on children of the root prim
    print(prim.GetPath())
```

Using [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) can be a powerful tool, but for large stages, more efficient and targeted methods should be considered.

Let's take a look at how we can traverse through the children of the default prim.

```{code-cell}

# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Open the USD stage from the specified file:
stage: Usd.Stage = Usd.Stage.Open("assets/tons_of_prims.usda")

# Get the default prim (primitive) of the stage:
default_prim: Usd.Prim = stage.GetDefaultPrim()

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Iterate through all children of the default prim
for child in default_prim.GetAllChildren():
    # Print the path of each child prim
    print(child.GetPath())

# Get a specific child prim named "Environment" under the default prim
child_prim: Usd.Prim = default_prim.GetChild("Environment")
# Print the details of the child prim
print(child_prim)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
```


### Example 4: Traversing using `Usd.PrimRange`

[`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) will return a [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) object. `UsdPrimRange` exposes pre- and post-order prim visitations allowing for a more involved traversals. It can also be used to perform actions such as pruning subtrees. [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) is a convenience method that performs visitations on all prims in the composed scenegraph that are active, defined, loaded, and concrete. It is recommended to use [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) over [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) for traversals.

Let's see an example of [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) in use.


```{code-cell}

# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("assets/tons_of_prims.usda")


# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

prim_range = Usd.PrimRange(stage.GetDefaultPrim())
for prim in prim_range:
    print(prim.GetPath())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
```

[`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178) will go through the entire stage. Unlike [`Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178), [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) can also traverse through a pseudo root prim. To do this, we'd pass the prim in question as an argument to the function. The code below demonstrates this:

```{code-cell}

# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("assets/tons_of_prims.usda")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

prim_range = Usd.PrimRange(stage.GetPrimAtPath("/World/Environment"))

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

for prim in prim_range:
    print(prim.GetPath())
```

There are other ways to use [`UsdPrimRange`](https://openusd.org/release/api/class_usd_prim_range.html) such as passing in [`predicates`](https://openusd.org/release/api/prim_flags_8h.html#Usd_PrimFlags), you can find more information in the [Using `Usd.PrimRange` in Python](https://openusd.org/release/api/class_usd_prim_range.html#details) section of `UsdPrimRange`.

### Example 5: Traversing a Stage

We can traverse a USD stage using [`Usd.Stage.Traverse()`](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178). This is fundamental when working with USD files, especially in complex 3D scenes and pipelines.

```{code-cell}

from pxr import Usd

file_path = "assets/second_stage.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

for prim in stage.Traverse():
    print(prim.GetPath())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
```

Traversing is done depth-first search and can be used to not just go throught the whole stage but a branch of the whole tree.


## Key Takeaways

Traversal is how we navigate the scenegraph and query scene data. Traversal can be made more efficient by limiting the number of prims it visits.

Let's try out some traversal functions in the next activity.



