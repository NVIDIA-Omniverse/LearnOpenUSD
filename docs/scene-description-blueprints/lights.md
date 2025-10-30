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
# Lights

In this lesson, we'll explore lights in OpenUSD, schemas belonging to the `UsdLux` domain. Understanding lights in OpenUSD allows for accurate and realistic lighting in 3D scenes.

## What Is UsdLux?

```{kaltura} 1_1ubiqm73
```

`UsdLux` is the schema domain that includes a set of light types and light-related schemas. It provides a standardized way to represent various types of lights, such as:

* Directional lights (`UsdLuxDistantLight`)
* Area lights, including 
    * Cylinder lights (`UsdLuxCylinderLight`)
    * Rectangular area lights (`UsdLuxRectLight`)
    * Disk lights (`UsdLuxDiskLight`)
    * Sphere lights (`UsdLuxSphereLight`)
* Dome lights (`UsdLuxDomeLight`)
* Portal lights (`UsdLuxPortalLight`)

### How Does It Work?

Start by defining light prims within a USD scene. These light primitives consist of scene description for specific light types (e.g., `UsdLuxDistantLight` for directional lights) and contain attributes that provide comprehensive control over the light's properties, such as intensity, color, and falloff. These light primitives allow for accurate lighting calculations during rendering.

### Working With Python

Here are a few relevant Python commands for working with USD lights:

```python
# Import the UsdLux module
from pxr import UsdLux
	
# Create a sphere light primitive
UsdLux.SphereLight.Define(stage, '/path/to/light')

# Set the intensity of a light primitive
light_prim.GetIntensityAttr().Set(500)
```

`UsdLux` has API schemas that allow you to add light behavior to prims in your scene, so you can also add light properties to meshes and volumes.

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: UsdLux and DistantLight

[`UsdLux`](https://openusd.org/release/api/usd_lux_page_front.html) is a USD lighting schema that provides a representation for lights.

One of the schemas in `UsdLux` is [`DistantLight`](https://openusd.org/release/api/class_usd_lux_distant_light.html). A light is emitted from a distance source along the -Z axis. This is commonly known as a directional light.

```{code-cell}
:emphasize-lines: 13-14
from pxr import Usd, UsdGeom, UsdLux

file_path = "_assets/distant_light.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# Define a new Scope primitive at the path "/World/Lights" on the current stage:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Lights"))

# Define a new DistantLight primitive at the path "/World/Lights/SunLight" on the current stage:
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("SunLight"))

stage.Save()
```
```{note}
The SunLight will not show up in the scene visually but it is displayed in the hierarchy.
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True)
```


### Example 2: Setting Light Properties

We're going to define two new prims, [`SphereLight`](https://openusd.org/dev/api/class_usd_lux_sphere_light.html) and [`DistantLight`](https://openusd.org/release/api/class_usd_lux_distant_light.html), and set a few properties for them.


```{code-cell}
:emphasize-lines: 12-32
from pxr import Gf, Usd, UsdGeom, UsdLux

file_path = "_assets/light_props.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath("Box"))

# Define a `Scope` Prim in stage at `/Lights`:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Lights")

# Define a `Sun` prim in stage as a child of `lights_scope`, called `Sun`:
distant_light = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("Sun"))
# Define a `SphereLight` prim in stage as a child of lights_scope called `SphereLight`:
sphere_light = UsdLux.SphereLight.Define(stage, lights_scope.GetPath().AppendPath("SphereLight"))

# Configure the distant light's emissive attributes:
distant_light.GetColorAttr().Set(Gf.Vec3f(1.0, 0.0, 0.0)) # Light color (red)
distant_light.GetIntensityAttr().Set(120.0) # Light intensity
# Lights are Xformable
if not (xform_api := UsdGeom.XformCommonAPI(distant_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
xform_api.SetRotate((45.0, 0.0, 0.0))
xform_api = None

# Configure the sphere light's emissive attributes:
sphere_light.GetColorAttr().Set(Gf.Vec3f(0.0, 0.0, 1.0)) # Light color (blue)
sphere_light.GetIntensityAttr().Set(50000.0) # Light intensity
# Lights are Xformable
if not (xform_api := UsdGeom.XformCommonAPI(sphere_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
xform_api.SetTranslate((5.0, 10.0, 0.0))

stage.Save()
```
```{note}
The lights will not show up in the scene visually but it is displayed in the hierarchy.
```
```{code-cell}
:tags: [remove-input]
DisplayUSD(file_path, show_usd_code=True, show_usd_lights=True)
```

## Key Takeaways

OpenUSD provides a standardized way to represent various types of lights in a USD scene to ensure consistent light behavior across different applications and renderers. They support different properties and attributes, and advanced
features like light filters, IES profiles and linking. Renderers can utilize USD’s lights and materials for accurate lighting calculations.

By understanding how to define and control lights within OpenUSD, developers and 3D practitioners can achieve realistic lighting, enhance visual quality, and unlock new possibilities in their projects.



