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
# Custom Properties

## What are Custom Properties?
Now, let's explore the concept of custom properties in Universal Scene Description. Understanding custom properties is essential for tailoring OpenUSD assets and workflows to specific needs, enabling more flexible and detailed scene descriptions.

Custom properties in OpenUSD are user-defined properties that can be added to prims to store additional data. Unlike schema attributes, which are predefined and standardized, custom attributes allow users to extend the functionality of OpenUSD to suit their specific requirements.

### How Does It Work?

#### Custom schemas vs. custom attributes

Custom schemas are a more advanced topic that we’ll cover in future lessons, but let’s compare the two briefly. When considering custom attributes versus custom schemas, the main strengths of custom attributes are their ease of use, and ability to be defined at any time, by any type of user. The main strengths
of custom schemas are their ability to group related information, and provide standardization.

For instance, consider we’re creating a web page for ordering a cake. One approach would be to create a single large, scrollable text field that we can assign a label to, like “What kind of cake do you need”, and let the user enter whatever they want in it.

Another approach might be to create a form with multiple fields, each of which is designed to store a very specific piece of information: what kind of cake, what type of icing, what size, if they want sprinkles, what should be written on top...

The first approach, the single text field, is similar to custom attributes. It allows the user to decide the information they want to enter. It’s also easier--if you’re new to working with USD, or need to implement custom fields very quickly, this might be the way to go.

On the other hand, custom schemas allow us to define a group of data in a more standardized way. However, it requires more planning and consideration, what fields we collect are predefined, and it takes longer to implement.

---

With that, let’s get back to our lesson on custom attributes.

Custom attributes are created and managed using the USD API. They can hold various types of data, such as numeric values, strings, or arrays, and can be sampled over time. This flexibility makes them useful for a wide range of applications, from simple metadata storage to complex animations.

Here are a few ways we can use custom attributes to enhance our OpenUSD workflows:

* **Metadata storage** : Storing additional information about a prim, such as author names, creation dates, or custom tags. 
* **Animation data** : Defining custom animation curves or parameters that are not covered by standard schema attributes.
* **Simulation parameters** : Storing parameters for physics simulations or other procedural generation processes. 
* **Arbitrary end user data** : Because they can be easily defined at run time, custom attributes are the best way to allow end users to define arbitrary custom data.

Custom attributes are the easiest and most flexible way to adapt OpenUSD to specific workflows and requirements, making it a powerful tool for industries like manufacturing, product design, architecture, and engineering, wherever we have multiple data types from many sources with varying purposes--like connecting our OpenUSD to sensor data or IoT for live, connected digital twins, or creating a production model with attributes like part numbers, manufacturer, life cycle costs, and even carbon data that can sync 3D scene description to 2D project documents, like a bill of materials or carbon emission calculators.

### Working With Python

![Custom Attribute Python](../images/CustomAttribute_Python.webm)

Here’s an example where we’re creating a custom attribute to add a serial number and last maintenance date to a prim, so a supervisor can easily identify which machines are due for maintenance from the 3D model.

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/ExamplePrim", "Xform")
serial_num_attr = prim.CreateAttribute("serial_number", Sdf.ValueTypeNames.String)

assert serial_num_attr.IsCustom()

mtce_date_attr = prim.CreateAttribute("maintenance_date", Sdf.ValueTypeNames.String)
serial_num_attr.Set("qt6hfg23")
mtce_date_attr.Set("20241004")

print(f"Serial Number: {serial_num_attr.Get()}")
print(f"Last Maintenance Date: {mtce_date_attr.Get()}")
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Adding Attributes to a Prim

[`Attributes`](https://openusd.org/release/glossary.html#attribute) are the most common type of property authored in most USD scenes. An attribute consist of a type and default value. It can also include time sampled values.

Here is an example of a `Cube` prim with an attribute called `weight`:

```usda
def Cube "Box" 
{
    double weight = 50
}
```

```{code-cell}

from pxr import Usd, UsdGeom

file_path = "assets/second_stage.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Get the Cube prim at path: `/Geometry/GroupTransform/Box`:
cube: UsdGeom.Cube = UsdGeom.Cube(stage.GetPrimAtPath("/Geometry/GroupTransform/Box"))
# Get all attribute names associated with Cube:
cube_attrs = cube.GetSchemaAttributeNames()
# Print out all the attribute names for Cube:
for attr in cube_attrs:
    print(attr)
# Get the Attribute for "Display Color":
cube_color_attr: Usd.Attribute = cube.GetDisplayColorAttr()
# Set the "Display Color" attribute to red:
cube_color_attr.Set([(1.0, 0.0, 0.0)])

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

To see all attributes defined by a schema we used [`GetSchemaAttributeNames()`](https://openusd.org/release/api/class_usd_geom_cube.html#a7c62fe4bca24edb5beae756618bf602f). Each schema will contain their own predetermined attributes.

After retrieving the attribute we can set the value using [`Set()`](https://openusd.org/release/api/class_usd_attribute.html#a7fd0957eecddb7cfcd222cccd51e23e6). Getting the attribute does not mean we are retrieving the value of the attribute.

### Example 2: Creating Additional Attributes

For custom attributes that are not apart of any schema, we use the [`CreateAttribute()`](https://openusd.org/release/api/class_usd_prim.html#ab86d597d65ae87c10b14746bec306100) method.

Custom attributes in OpenUSD are used to define additional, user-specific properties for objects within a 3D scene. These attributes extend beyond the standard properties like position, rotation, and color, allowing creators to add unique data relevant to their specific needs. For example, custom attributes can store information such as material properties, animation controls, or metadata for a particular workflow. 

When creating an attribute in OpenUSD, we need to specify the type of the attribute. For example, we can create a `float` attribute for the weight of the box:

```python
box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float)
```

[`ValueTypeNames`](https://openusd.org/release/api/class_sdf_value_type_name.html) represent an attribute's type. These are defined in [`Sdf`](https://openusd.org/release/api/sdf_page_front.html) and more types can be found in OpenUSD's [documentation](https://openusd.org/release/api/sdf_page_front.html#sdf_metadata_types).


```{code-cell}

from pxr import Usd, UsdGeom, Sdf

file_path = "assets/custom_attributes.usda"
stage: Usd.Stage = create_new_stage(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("box/cubebox_a02_distilled/cubebox_a02_distilled.usd")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Create additional attributes for the box prim
box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float, custom=True)
box_prim.CreateAttribute("size_cm", Sdf.ValueTypeNames.Float, custom=True)
box_prim.CreateAttribute("type", Sdf.ValueTypeNames.String, custom=True)
box_prim.CreateAttribute("hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


# Save the stage
stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

### Example 3: Modifying Custom Attributes

After creating an attribute, we can set and get the value of the attribute, similar to what we did in the previous activity. 

Try applying the same logic to the other attributes.

```{code-cell} 

from pxr import Usd, UsdGeom, Sdf

file_path = "assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)


world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("box/cubebox_a02_distilled/cubebox_a02_distilled.usd")

box_prim.CreateAttribute("size_cm", Sdf.ValueTypeNames.Float, custom=True)
box_prim.CreateAttribute("type", Sdf.ValueTypeNames.String, custom=True)
box_prim.CreateAttribute("hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Defining the weight attribute
box_weight_attr: Usd.Attribute = box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float, custom=True)
# Set the value of the weight attribute
box_weight_attr.Set(50)

# Print the weight of the box
print("Weight of Box:", box_weight_attr.Get())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

## Key Takeaways

Custom attributes in OpenUSD provide a versatile way to extend the functionality of scene descriptions, making them adaptable to various specialized needs. By understanding how to create, set, and retrieve custom attributes, we can enhance our OpenUSD workflows and better manage complex data in our projects, significantly improve the precision and efficiency of digital models, and build USD pipelines that are tailored to specific use
cases.



