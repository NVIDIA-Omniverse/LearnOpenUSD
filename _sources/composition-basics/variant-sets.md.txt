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

orphan: true
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
# Variant Sets Basics

## What Are Variant Sets?

### How Does It Work?


### Working With Python

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
from utils.helperfunctions import create_new_stage
```

### Setup

Before we begin, let's create a USD stage using the [`stage`](https://openusd.org/release/glossary.html#usdglossary-stage) class from the `Usd` module.


**Run the cell below to create a new USD Stage.** This will setup a stage that contains a variety of prims of different schemas. We'll use this content to demonstrate how to build `VariantSets` in the rest of this lesson.

```{code-cell} ipython3
:cell_id: cd045f5221c549f7bc2264d5f28bbc53
:deepnote_cell_type: code
:deepnote_to_be_reexecuted: false
:execution_millis: 1368
:execution_start: 1716843480676
:source_hash: null

from pxr import Usd, UsdGeom

stage: Usd.Stage = create_new_stage("_assets/variant_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))

stage.Save()
DisplayUSD("_assets/variant_prims.usda", show_usd_code=True)
```

### Example 1: Verifying VariantSets Exist

A [`variantSet`](https://openusd.org/release/glossary.html#usdglossary-variantset) is like a group of options that you can apply to a single item (called a "prim"). Imagine it as a switch that lets a content creator bundle different choices together. This way, someone using the content later can easily switch between these options or add new ones without changing the original item.

To check if a variantSet exists, use the [`HasVariantSets()`](https://openusd.org/release/api/class_usd_prim.html#a87443b32a72f95ca96d960b4e96cbf02) method.

**Run the cell below to check if the variantSet exists in the `variant_prims.usda` we created in the previous cell.**

```{code-cell} ipython3
:cell_id: 08a7076a78cf4326803977fa2cd6a650
:deepnote_cell_type: code
:deepnote_to_be_reexecuted: false
:execution_millis: 90
:execution_start: 1716843683212
:source_hash: null

from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# Get the prim at the specified path:
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# Print whether the prim has variant sets:
print(geo_scope.HasVariantSets())
```

+++ {"cell_id": "0d9565a9733a4279a42fbeef6beea7e0", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

---

### Example 2: Adding a VariantSet and Variants

[`Variants`](https://openusd.org/release/glossary.html#usdglossary-variant) can hold different settings or details, like properties or metadata, and even entire sections of a scene. A variant is just one specific version within a group called a variantSet. Each variantSet can have one or none of these versions selected in a scene.

To create a variantSet, it needs to have at least one variant in the variantSet. 

To get all varaintSets, we would use [`GetVariantSets()`](https://openusd.org/release/api/class_usd_prim.html#a607da249e11bc4f5f3b4bf0db99861ab). 

To add a variantSet, we'd use [`AddVariantSet()`](https://openusd.org/release/api/class_usd_variant_sets.html#afa72971becc14b53366f2913307b8164). 

For adding variants to the variantSet, we would use [`AddVariant()`](https://openusd.org/release/api/class_usd_variant_set.html#a13cac327430d050108a8c22cada16b45).

A small example on how to use the methods can be found below:

```python
from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# Get the prim at the specified path:
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# Get the "shapes" variant set for the geometry scope:
geo_variant_sets = geo_scope.GetVariantSets()
shapes_variant_set = geo_variant_sets.AddVariantSet("shapes")

# Add a variant named "Cube" to the "shapes" variant set:
geo_variant_set.AddVariant("Cube")

# Print whether the geometry scope now has variant sets:
print(geo_scope.HasVariantSets())

# Save the changes to the stage:
stage.Save()
```

+++

Let's add some variants to the `shapes` variant set.

**Add the following code to the cell below, then run the cell:**

```python
geo_variant_sets = geo_scope.GetVariantSets()
shapes_variant_set = geo_variant_sets.AddVariantSet("shapes")
for shape in shapes:
    shapes_variant_set.AddVariant(shape)
```

```{code-cell} ipython3
:cell_id: aacd8a169ad84c1ea7472c47a830fd77
:deepnote_cell_type: code
:deepnote_to_be_reexecuted: false
:execution_millis: 607
:execution_start: 1716842406788
:source_hash: null

from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# List of shapes to add as variants:
shapes = ["Cube", "Sphere", "Cylinder", "Cone"]

# Get the prim at the specified path "/World/Box/Geometry":
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


# Save the changes to the stage:
stage.Save()
# Print the unflattened Root Layer:
DisplayUSD("_assets/variant_prims.usda", show_usd_code=True)
```

+++ {"cell_id": "0226b2538b4640a5b479ddbe87948ff4", "deepnote_app_block_visible": false, "deepnote_cell_type": "markdown"}

---

### Example 3: Modifying Variants

To edit a variant, switch to it by using the [`SetVariantSelection()`](https://openusd.org/release/api/class_usd_variant_set.html#a51fe1abe65de6440b81799393b1a424f) method. Then, we can edit the variant and make our changes, such as modifying properties or adding new details. 

In our case, we will be modifying what shape will be defined under the geometry scope.

**Add the following code to the cell below, then run the cell:**

```python
# Loop over each shape in the list of shapes
for shape in shapes:
    # Print the shape being added
    print("adding: " + shape)
    
    # Add a variant named after the shape to the "shapes" variant set
    shapes_variant_set.AddVariant(shape)
    
    # Select the current variant for editing
    shapes_variant_set.SetVariantSelection(shape)
    
    # Enter the variant edit context to make changes specific to the current variant
    with shapes_variant_set.GetVariantEditContext():
        # Define a new prim for the current shape under the geometry scope
        shape_prim = stage.DefinePrim(geo_scope.GetPath().AppendPath(shape))
        
        # Set the type of the new prim to the current shape
        shape_prim.SetTypeName(shape)
```

```{code-cell} ipython3
:cell_id: a68b823a695247228a8837a69d73851b
:deepnote_cell_type: code
:deepnote_to_be_reexecuted: false
:execution_millis: 678
:execution_start: 1716843398636
:source_hash: null

from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# List of shapes to add as variants:
shapes = ["Cube", "Sphere", "Cylinder", "Cone"]

# Get the prim at the specified path "/World/Box/Geometry":
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# Get the "shapes" variant set for the geometry scope:
geo_variant_sets = geo_scope.GetVariantSets()
shapes_variant_set = geo_variant_sets.AddVariantSet("shapes")
    
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


# Here we define what Variant from the VariantSet is selected. Change this between "Cube", "Sphere", "Cylinder", and "Cone"
# to see the different geometries:
shapes_variant_set.SetVariantSelection("Cube")
# shapes_variant_set.SetVariantSelection("Sphere")
# shapes_variant_set.SetVariantSelection("Cylinder")
# shapes_variant_set.SetVariantSelection("Cone")

# Save the changes to the stage
stage.Save()
DisplayUSD("_assets/variant_prims.usda", show_usd_code=True)
```

In OpenUSD, `VariantSets` and `Variants` enable the creation of flexible, dynamic scenes by allowing multiple versions of models or components to coexist within a single scene graph. This facilitates efficient asset management, easy customization, and the ability to switch between different configurations seamlessly.

## Key Takeaways