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

## What Are Custom Properties?
Now, let's explore the concept of custom properties in Universal Scene Description. Understanding custom properties is essential for tailoring OpenUSD assets and workflows to specific needs, enabling more flexible and detailed scene descriptions.

Custom properties in OpenUSD are user-defined properties that can be added to prims to store additional data. Unlike schema attributes, which are predefined and standardized, custom attributes allow users to extend the functionality of OpenUSD to suit their specific requirements.

## How Does It Work?

### Custom schemas vs. custom properties

Custom schemas are a more advanced topic that we’ll cover in future lessons, but let’s compare the two briefly. When considering custom properties versus custom schemas, the main strengths of custom properties are their ease of use and ability to be defined at any time. The main strengths of custom schemas are their ability to group related information and provide standardization.

For instance, consider we’re creating a web page for ordering a cake. One approach would be to create a single large, scrollable text field that we can assign a label to, like “What kind of cake do you need?”, and let the user enter whatever they want in it.

Another approach might be to create a form with multiple fields, each of which is designed to store a very specific piece of information: what kind of cake, what type of icing, what size, if they want sprinkles, what should be written on top...

The first approach, the single text field, is similar to custom properties. It allows the user to decide the information they want to enter. It’s also easier--if you’re new to working with USD, or need to implement custom fields very quickly, this might be the way to go.

On the other hand, custom schemas allow us to define a group of data in a more standardized way. However, it requires more planning and consideration, what fields we collect are predefined, and it takes longer to implement.

---

With that, let’s get back to our lesson on custom properties.

Custom properties are created and managed using the USD API. They can work just like schema attributes and relationships. Custom attributes are more common because they can hold various types of data, such as numeric values, strings, or arrays, and can be sampled over time.This flexibility makes them useful for a wide range of applications, from simple metadata storage to complex animations.

Here are a few ways we can use custom properties to enhance our OpenUSD workflows:

* **Metadata storage** : Storing additional information about a prim, such as author names, creation dates, or custom tags. 
* **Animation data** : Defining custom animation curves or parameters that are not covered by standard schema properties.
* **Simulation parameters** : Storing parameters for physics simulations or other procedural generation processes. 
* **Arbitrary end user data** : Because they can be easily defined at run time, custom properties are the best way to allow end users to define arbitrary custom data.

Custom properties are the easiest and most flexible way to adapt OpenUSD to specific workflows and requirements, making it a powerful tool for industries like manufacturing, product design, architecture, and engineering, wherever we have multiple data types from many sources with varying purposes--like connecting our OpenUSD to sensor data or IoT for live, connected digital twins, or creating a production model with attributes like part numbers, manufacturer, life cycle costs, and even carbon data that can sync 3D scene description to 2D project documents, like a bill of materials or carbon emission calculators.

```{note}
We often recommend custom properties instead of metadata or `customData` metadata for prototyping because the former requires plugin-based schema development which is less portable and the later is more costly for composition because it is a composable dictionary data type.
```

## Working With Python

![Custom Attribute Python](../images/foundations/CustomAttribute_Python.webm)

Here’s an example where we’re creating a custom attribute to add a serial number and last maintenance date to a prim, so a supervisor can easily identify which machines are due for maintenance from the 3D model.

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/ExamplePrim", "Xform")
serial_num_attr = prim.CreateAttribute("my_namespace:serial_number", Sdf.ValueTypeNames.String, custom=True)

assert serial_num_attr.IsCustom()

mtce_date_attr = prim.CreateAttribute("my_namespace:maintenance_date", Sdf.ValueTypeNames.String, custom=True)
serial_num_attr.Set("qt6hfg23")
mtce_date_attr.Set("20241004")

print(f"Serial Number: {serial_num_attr.Get()}")
print(f"Last Maintenance Date: {mtce_date_attr.Get()}")
```

For custom attributes that are not a part of any schema, we use the {usdcpp}`UsdPrim::CreateAttribute` method. {usdcpp}`ValueTypeNames <SdfValueTypeName>` represent an attribute's type. These are defined in {usdcpp}`Sdf <sdf_page_front>` and more types can be found in OpenUSD's [documentation](https://openusd.org/release/api/sdf_page_front.html#sdf_metadata_types).


Setting `custom=True` has no impact on the way that OpenUSD treats the attribute, but it is a useful piece of metadata to inform end-users and developers that a particular attribute is not part of an existing schema.

Lastly, notice the `my_namespace:` prefix on the attribute. It's good practice to namespace custom properties and schemas created by your organization. This helps avoid name clashes and it helps the ecosystem understand where content orginated from. For NVIDIA custom properties, we use the `omni:` namespace for example.

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Creating Custom Attributes

+++ {"tags": ["remove-cell"]}
>**NOTE**: Run the cell below copy the required asset to the right location for the example.
+++
```{code-cell}
:tags: [remove-input, remove-output]
import shutil
# cleanup any existing copy
try:
    shutil.rmtree('_assets/cubebox_a02')
except FileNotFoundError:
    pass
shutil.copytree('../exercise_content/foundations/cubebox_a02', '_assets/cubebox_a02')
```


Custom attributes in OpenUSD are used to define additional, user-specific properties for objects within a 3D scene. These attributes extend beyond the standard attributes like position, rotation, and color, allowing creators to add unique data relevant to their specific needs. For example, custom attributes can store information such as material properties, animation controls, or metadata for a particular workflow. 

In this example, we will author custom attributes to add more contextual information to a package asset.

```{code-cell}
:emphasize-lines: 13-23

from pxr import Usd, UsdGeom, Sdf

file_path = "_assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Packages"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("./cubebox_a02/cubebox_a02.usd")

# Create additional attributes for the box prim
weight = box_prim.CreateAttribute("acme:weight", Sdf.ValueTypeNames.Float, custom=True)
category = box_prim.CreateAttribute("acme:category", Sdf.ValueTypeNames.String, custom=True)
hazard = box_prim.CreateAttribute("acme:hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# Optionally document your custom property
weight.SetDocumentation("The weight of the package in kilograms.")
category.SetDocumentation("The shopping category for the products this package contains.")
hazard.SetDocumentation("Whether this package contains hazard materials.")

# Set values for the attributes
weight.Set(5.5)
category.Set("Cosmetics")
hazard.Set(False)

# Save the stage
stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

You can use {usdcpp}`UsdObject::SetDocumentation` to document your content. This documentation string can be presented to end users as tooltips or other UIs in applications so they understand how to author or use the data.

### Example 2: Modifying Custom Attributes

After creating an attribute, we can set and get the value of the attribute, similar to what we did in the previous example. 

Try applying the same logic to the other attributes.

```{code-cell} 
:emphasize-lines: 7-10

from pxr import Usd, UsdGeom, Sdf

file_path = "_assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)
box_prim = stage.GetPrimAtPath("/World/Packages/Box")

# Get the weight attribute
weight_attr: Usd.Attribute = box_prim.GetAttribute("acme:weight")
# Set the value of the weight attribute
weight_attr.Set(4.25)

# Print the weight of the box
print("Weight of Box:", weight_attr.Get())

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```

## Key Takeaways

Custom properties in OpenUSD provide a versatile way to extend the functionality of scene descriptions, making them adaptable to various specialized needs. By understanding how to create, set, and retrieve custom properties, we can enhance our OpenUSD workflows and better manage complex data in our projects, significantly improve the precision and efficiency of digital models, and build USD pipelines that are tailored to specific use
cases.



