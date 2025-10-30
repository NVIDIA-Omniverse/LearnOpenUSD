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

# Schemas

![Schema Definition](../images/foundations/Schema_Definition.webm)

Schemas give meaning to prims in OpenUSD, i.e., “What is this element? What capabilities does it have?”. Schemas define the data models and optional API for encoding and interchanging 3D and non-3D concepts through OpenUSD.

We'll explore the different types of schemas, their characteristics, and how they enable the creation of sophisticated virtual worlds and digital twins.

## What Are Schemas?

Schemas serve as blueprints that author and retrieve data, like attributes and relationships that govern behaviors of elements in a USD scene. They provide a consistent and extensible way to define and interpret data, ensuring data interoperability between different software tools and applications.

Each prim in a scene is an element that implicitly contains the properties and fallback values of the typed schema that’s telling the prim what it is. For example, the `radius` attribute for the `Sphere` schema is defined as `double radius = 1` meaning that all Sphere prims have a radius represented by a double-precision floating point number with a value of `1` by default.

Schemas are primarily data models with documented rules on how the data should be interpreted. While schemas define the structure and rules, they do not necessarily include the implementation of behaviors. For example, the `UsdPhysics` schemas does not come with a physics engine. Developers may provide behaviors in the schema API, but this is not a requirement.

There is a trend toward codeless schemas for easier distribution, suggesting that schemas might become more lightweight, focusing on data modeling rather than behavior implementation.

Actual behavior enforcement can be managed by other subsystems within the runtime ecosystem. This allows for flexibility and performance optimization based on different use cases.

There are two types of schemas used with OpenUSD: IsA schemas and API schemas. Let’s talk about IsA schemas first.

### IsA Schemas

IsA schemas, also known as Typed schemas or Prim schemas, essentially tell a prim what it is. Because of this, each prim can only subscribe to one IsA schema at a time.

We use the `typeName` metadata to assign an IsA schema to a prim.  

IsA schemas are derived from the core class `UsdTyped`, the base class for all typed schemas, which is why we hear IsA schemas referred to as "typed" schemas.

These schemas can either be concrete (instantiable) or abstract (non-concrete, serve as base classes). We refer to a schema as concrete when the schema can be instantiated as prims in the USD scene, as we see with `UsdGeomMesh` and `UsdGeomScope`. Concrete schemas provide both a name and a typeName in the schema definition.

Meanwhile, abstract, or non-concrete schemas, provide a name but no typeName in the schema definition. This enables them to serve as a base class for related sets of concrete schemas, the way `UsdGeomPointBased` serves as a base class for geometric objects that contain points, like meshes (`UsdGeomMesh`), or basis curves (`UsdGeomBasisCurves`).

### API Schemas

In addition to IsA schemas, we have API schemas. API schemas are similar to IsA schemas except it does not specify a typeName. Since it does not have a typeName they are considered to be non-concrete.

API schemas are typically named with the suffix “API” in their C++ or Python class name, such as `UsdShadeConnectableAPI`. Properties that belong to an API schema are namespaced with the schemas base name and camelCased. For example, `UsdPhysics.RigidBodyAPI.CreateVelocityAttr()` will create an attribute named `physics:velocity`.

API schemas can be classified as non-applied or applied schemas, and single-apply or multiple-apply, where single-apply API schemas are applied to only a single instance of a prim, and multiple-apply API schemas can be applied multiple times to the same prim with different instance names.

Unlike IsA schemas, API schemas do not assign a typeName to a prim. Instead, are list-edited in the `apiSchemas` metadata and queryable via the `HasAPI` method. API schemas are assigned to already-typed prims to annotate them with additional properties that govern behaviors.



### Working With Python

![Schema Python](../images/foundations/Schema_Main.webm)

In Python, we can work with schemas using the following methods:

```python
# Retrieve the schema info for a registered schema
Usd.SchemaRegistry.FindSchemaInfo()

# Retrieve the schema typeName
Usd.SchemaRegistry.GetSchemaTypeName()
```

These methods allow us to interact with and manipulate schemas programmatically, enabling us to create, modify, and validate USD assets based on predefined rules and conventions.

Let’s look at some common built-in schemas that will come up as we are learning about OpenUSD.

#### IsA Schemas

##### UsdGeomSphere

![Schema USDGeom](../images/foundations/Schema_UsdGeom.webm)

`UsdGeom` defines schemas for representing geometric objects, such as meshes, cameras, and curves as mentioned above. It also includes schemas for transformations, visibility, and other common properties.

```python
# Import related classes
from pxr import UsdGeom

# Define a sphere in the stage
sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
	
# Get and Set the radius attribute of the sphere
sphere.GetRadiusAttr().Set(10)
```

##### UsdLuxDiskLight

![Schema UsdLux](../images/foundations/Schema_UsdLux.webm)

`UsdLux` defines schemas for representing light sources in a scene. It includes schemas such as sphere lights, disk lights, and distant lights, which were discussed in the lesson on USD lights.

Examples include `UsdLuxDiskLight`, `UsdLuxRectLight`, and `UsdLuxSphereLight`.

```python
# Import related classes
from pxr import UsdLux

# Define a disk light in the stage
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")
	
# Get all Attribute names that are a part of the DiskLight schema
dl_attribute_names = disk_light.GetSchemaAttributeNames()
	
# Get and Set the intensity attribute of the disk light prim
disk_light.GetIntensityAttr().Set(1000)
```

#### API Schemas

##### UsdPhysicsRigidBodyAPI

![Schema UsdPhysics](../images/foundations/Schema_UsdPhysics.webm)

`UsdPhysicsRigidBodyAPI` adds physics properties to any `UsdGeomXformable` object for simulation such as rigid body dynamics.

```python
# Import related classes
from pxr import UsdPhysics

# Apply a UsdPhysics Rigidbody API on the cube prim
cube_rb_api = UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
	
# Get the Kinematic Enabled Attribute 
cube_rb_api.GetKinematicEnabledAttr()
	
# Create a linear velocity attribute of value 5
cube_rb_api.CreateVelocityAttr(5)
```

This example shows how API schemas can be applied to prims to add specific properties that govern behaviors, such as adding rigid body capabilities to an object hierarchy.

## Key Takeaways

Schemas in OpenUSD serve as templates for defining prims. It's worth noting there are actually two distinct types of schemas: IsA and API schemas. API schemas work alongside IsA schemas to provide a flexible and extensible system for building complex scenes in OpenUSD.

Schemas are a complex topic, but when leveraged correctly, they can simplify the creation and interchange of USD scenes. We’ll cover schemas again, including custom schemas, in future lessons.



