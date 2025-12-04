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

# Attributes

## What Is an Attribute?

```{kaltura} 1_u0uzffig
```

{term}`Attributes <Attribute>` are the most common type of {term}`property <Property>` that you'll work with when creating scenes. An attribute can have one specific data type, such as a number, text, or a vector. Each attribute can have a {term}`default value <Default Value>`, and it can also have different values at different points in time, called {term}`time samples <Time Sample>`.

### How Does It Work?

Attributes are name-value pairs (often referred to as key-value pairs) that store data associated with a {term}`prim <Prim>`.

Any given attribute has a single, defined data type associated with it. Each attribute is defined with the type of data that it can hold. A single attribute can represent various types of properties, such as the vertices of a piece of geometry, the diffuse color of a material, or the mass of an object. These are typically defined through the `Sdf` library.

Some common examples of attributes include:

* **{term}`Visibility <Visibility>`** - Controls the visibility of a prim in the scene.
* **Display color** - Specifies the display color applied to a geometric prim.
* **Extent** - Defines the boundaries of a geometric prim. 

Attributes can be authored and stored within USD {term}`layers <Layer>`, which are files that describe different aspects of a scene. When a USD {term}`stage <Stage>` is composed, the attribute values from various layers are combined according to specific {term}`composition <Composition>` rules, allowing for flexible scene assembly.

Attributes can be {term}`animated <Animated Value>` by providing multiple keyframed values over time. OpenUSD's timeSampling model ensures efficient storage and interpretation of animated data. We will learn more about time samples in the {doc}`../timecodes-timesamples` lesson.

### Working With Python

To work with attributes in OpenUSD, we will generally use schema-specific APIs. Each schema-specific API has a function to grab its own attributes. Review the following examples to learn more.

```python
# Get the radius value of sphere_prim that is of type UsdGeom.Sphere
sphere_prim.GetRadiusAttr().Get()

# Set the double-sided property of the prim
sphere_prim.GetDoubleSidedAttr().Set(True)
```

While there’s also a dedicated `UsdAttribute` API, in general, it's preferred to use the schema-specific methods, if they exist, as they are more clear and
less brittle. You can learn more about how to work with each specific schema on OpenUSD’s [documentation](https://openusd.org/release/api/annotated.html).

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
from utils.helperfunctions import create_new_stage
```

### Example 1: Retrieving Properties of a Prim 

Properties are the other kind of namespace object in OpenUSD. Whereas prims provide the organization and indexing for a composed scene, properties contain the "real data". 

There are two types of properties: attributes and relationships.

To retrieve the properties of a prim, we would use the [`GetProperties`](https://openusd.org/release/api/class_usd_prim.html#aa3d8915481ff6280c22c60de4a833423) method. For this demonstration we will be using [`GetPropertyNames()`](https://openusd.org/release/api/class_usd_prim.html#a24377e6ababf44be9534a68046ebb7b8) instead to retrieve the names of the properties. This will not grab the properties themselves, but a list of the names of the properties. Use [`GetProperties`](https://openusd.org/release/api/class_usd_prim.html#aa3d8915481ff6280c22c60de4a833423) to retrieve the properties themselves.


```{note}
Relationships are only lightly discussed in this lesson. We'll talk about relationships again in the {doc}`relationships` lesson.
```

```{code-cell}
:emphasize-lines: 9-21

from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex1.usda"

stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a sphere under the World xForm:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))

# Define a cube under the World xForm and set it to be 5 units away from the sphere:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the property names of the cube prim:
cube_prop_names = cube.GetPrim().GetPropertyNames()

# Print the property names:
for prop_name in cube_prop_names:
    print(prop_name)

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

### Example 2: Getting Attribute Values

Attributes are the most common type of property authored in most USD scenes. 

An example of a simple attribute that describes the radius of a sphere:

```usda
def Sphere "Sphere"{
    double radius = 10
}
```

We interact with attributes through the [`UsdAttribute` API](https://openusd.org/release/api/class_usd_attribute.html).

Each prim type has their own set of properties and corresponding functions to retrieve them. Since our sphere is of type [`UsdGeom.Sphere`](https://openusd.org/release/api/class_usd_geom_sphere.html), we can use the schema-specific API to get and set the radius attribute.

[`GetRadiusAttr()`](https://openusd.org/release/api/class_usd_geom_sphere.html#abae017e4bd8775bc725d7df41317df85) will return a [`UsdAttribute`](https://openusd.org/release/api/class_usd_attribute.html) object that can be used to modify the attribute. Which means it will not retrieve the value of the attribute. To get the value of an attribute, use the [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9) method.

For example, to get the value of the radius attribute, we would use the following snippet.

```python
sphere_prim.GetRadiusAttr().Get()
```

Let's use the [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9) method for the `radius`, `displayColor`, and `extent` attributes.

Since we have not explicitly authored any attribute values, [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9) will return the fallback value that was defined in the schema. 

```{note}
The attribute values will not show up in `.usda`, however the values are coming from the fallback value defined in the sphere schema. USD is applying {term}`value resolution <Value Resolution>` to retrieve the values.
```

```{code-cell}
:emphasize-lines: 12-24

from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex2.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the attributes of the cube prim
cube_attrs = cube.GetPrim().GetAttributes()
for attr in cube_attrs:
    print(attr)

# Get the size, display color, and extent attributes of the cube
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

print(f"Size: {cube_size.Get()}")
print(f"Display Color: {cube_displaycolor.Get()}")
print(f"Extent: {cube_extent.Get()}")

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

### Example 3: Setting Attribute Values

In the last example, we used the [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9) method to retrieve the value of the attribute. To set the values, we use the [`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a151e6fde58bbd911da8322911a3c0079) method.

Here is an example of setting a value to the radius attribute.

```python
sphere_prim.GetRadiusAttr().Set(100.0)
```

When run, it will modify the sphere in the example scene to look like this:

```usda
def Sphere "Sphere"{
    double radius = 100
}
```

Based on our last modification, if we were to use [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9) it would return `100`.

When getting attribute values, USD will apply {term}`value resolution <Value Resolution>` since we authored a default value. The [`Get()`](https://openusd.org/release/api/class_usd_attribute.html#a9d41bc223be86408ba7d7f74df7c35a9) method will retrieve the value of the attribute. To set the values, we use the [`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a151e6fde58bbd911da8322911a3c0079) method. This will resolve to the authored value rather than the fallback value from the sphere schema.

Now let's modify the `size`, `displayColor`, and `extent` attributes of the cube by using [`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a151e6fde58bbd911da8322911a3c0079).

```{code-cell}
:emphasize-lines: 17-20

from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex3.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5,0,0))

# Get the size, display color, and extent attributes of the cube
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

# Modify the size, extent, and display color attributes:
cube_size.Set(cube_size.Get() * 2)
cube_extent.Set(cube_extent.Get() * 2)
cube_displaycolor.Set([(0.0, 1.0, 0.0)])

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

## Key Takeaways

In summary,

* Attributes are values with a name and data type that define the properties of prims in a USD scene. 
* Attributes are the primary means of storing data in USD. 
* Each attribute has a single, defined data type.
* Attributes are authored and stored within USD layers, enabling efficient scene composition.
* Attributes can be animated by providing keyframed values over time.
* They can be queried, modified and animated using the USD API.

Understanding attributes is essential for creating rich and detailed 3D scenes, enabling efficient collaboration and interoperability across various tools and pipelines.



