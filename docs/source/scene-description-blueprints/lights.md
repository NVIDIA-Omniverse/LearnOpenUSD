---
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

## What is UsdLux?

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

### Example 1: UsdLux and DistantLight

[`UsdLux`](https://openusd.org/release/api/usd_lux_page_front.html) is a USD lighting schema that provides a representation for lights.

One of the classes in `UsdLux` is [`DistantLight`](https://openusd.org/release/api/class_usd_lux_distant_light.html). A light is emitted from a distance source along the -Z axis. This is commonly known as a directional light.

`UsdLux` is another example of a schema-specific API.

**Add the following code to the cell below, then run the cell:**

```python
# Define a new Scope primitive at the path "/World/Environment" on the current stage:
env: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Environment"))

# Define a new DistantLight primitive at the path "/World/Environment/SkyLight" on the current stage:
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, env.GetPath().AppendPath("SkyLight"))
```

> **NOTE:** The Light will not show up in the scene visually but it is displayed in the hierarchy.

```{code-cell}

from pxr import Usd, UsdGeom, UsdLux, UsdShade

stage: Usd.Stage = Usd.Stage.Open("assets/many_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()
DisplayUSD("assets/many_prims.usda", show_usd_code=True)
```

### Example 2: Lighting a Stage

So far we have created prims using [`UsdGeom`](https://openusd.org/release/api/usd_geom_page_front.html). This is a [`schema`](https://openusd.org/release/glossary.html#usdglossary-schema) that defines 3D graphics-related prim and property schemas. USD also comes with other schemas, like [`UsdLux`](https://openusd.org/release/api/usd_lux_page_front.html) which provides a representation for lights and related components.

We're going to define two new prims: [`SphereLight`](https://openusd.org/dev/api/class_usd_lux_sphere_light.html) and [`DistantLight`](https://openusd.org/release/api/class_usd_lux_distant_light.html)

**Add the following code to the cell below, then run the cell:**
   
```python
# Define a `Scope` Prim in stage at `/Lights`:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Lights")
# Define a `Sun` prim in stage as a child of `lights_scope`, called `Sun`:
distant_light = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("Sun"))
# Define a `SphereLight` prim in stage as a child of lights_scope called `SphereLight`:
sphere_light = UsdLux.SphereLight.Define(stage, lights_scope.GetPath().AppendPath("SphereLight"))

# Configure the distant light's emissive attributes:
distant_light.GetColorAttr().Set(Gf.Vec3f(1.0, 0.0, 0.0)) # Light color (red)
distant_light.GetIntensityAttr().Set(120.0) # Light intensity
# Position the distant light in the 3D scene:
distant_light_transform = distant_light.GetTransformOp()
if not distant_light_transform:
    distant_light_transform = distant_light.AddTransformOp()
distant_light_transform.Set(Gf.Matrix4d((pi/4, 0, -pi/4, 0), (0, 1, 0, 0), (pi/4, 0, pi/4, 0), (10, 0, 10, 1)))
distant_light.GetXformOpOrderAttr().Set([distant_light_transform.GetName()])

# Configure the sphere light's emissive attributes:
sphere_light.GetColorAttr().Set(Gf.Vec3f(0.0, 0.0, 1.0)) # Light color (blue)
sphere_light.GetIntensityAttr().Set(50000.0) # Light intensity
# Position the sphere light in the 3D scene:
sphere_light_transform = sphere_light.GetTransformOp()
if not sphere_light_transform:
    sphere_light_transform = sphere_light.AddTransformOp()
sphere_light_transform.Set(Gf.Matrix4d((pi/4, 0, pi/4, 0), (0, 1, 0, 0), (-pi/4, 0, pi/4, 0), (-10, 0, 10, 1)))
sphere_light.GetXformOpOrderAttr().Set([sphere_light_transform.GetName()])
```

```{code-cell}

from math import pi
from pxr import Gf, Usd, UsdGeom, UsdLux

file_path = "assets/second_stage.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath("GroupTransform"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath("Box"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()
DisplayUSD(file_path, show_usd_code=True, show_usd_lights=True)
```

Now our hierarchy looks like the following:

- Geometry
    - GroupTransform
        - Box
- Lights
    - Sun
    - SphereLight

We have introduced two new prims: [`UsdLux.SphereLight`](https://openusd.org/dev/api/class_usd_lux_sphere_light.html) and [`UsdLux.DistantLight`](https://openusd.org/release/api/class_usd_lux_distant_light.html).

## Key Takeaways

OpenUSD provides a standardized way to represent various types of lights in a USD scene to ensure consistent light behavior across different applications and renderers. They support different properties and attributes, and advanced
features like light filters, IES profiles and linking. Renderers can utilize USD’s lights and materials for accurate lighting calculations.

By understanding how to define and control lights within OpenUSD, developers and 3D practitioners can achieve realistic lighting, enhance visual quality, and unlock new possibilities in their projects.



