In this lesson, we'll explore lights in OpenUSD, schemas belonging to the `UsdLux` domain. Understanding lights in OpenUSD allows for accurate and realistic lighting in 3D scenes.

<@ nvfunc kaltura 1_1ubiqm73 @>

`USDLux` includes a set of light types and light-related schemas. It provides a standardized way to represent various types of lights, such as:

* Directional lights (`UsdLuxDistantLight`)
* Area lights, including 
    * Cylinder lights (`UsdLuxCylinderLight`)
    * Rectangular area lights (`UsdLuxRectLight`)
    * Disk lights (`UsdLuxDiskLight`)
    * Sphere lights (`UsdLuxSphereLight`)
* Dome lights (`UsdLuxDomeLight`)
* Portal lights (`UsdLuxPortalLight`)



### How Does It Work?

Start by defining light prims within a USD scene. These light primitives consist of scene description for specific light types (e.g., `UsdLuxDistantLight` for directional lights) and contain attributes that provide comprehensive control over the light's properties, such as intensity,
color, and falloff. These light primitives allow for accurate lighting calculations during rendering.

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

### Key Takeaways

OpenUSD provides a standardized way to represent various types of lights in a USD scene to ensure consistent light behavior across different applications and renderers. They support different properties and attributes, and advanced
features like light filters, IES profiles and linking. Renderers can utilize USD’s lights and materials for accurate lighting calculations.

By understanding how to define and control lights within OpenUSD, developers and 3D practitioners can achieve realistic lighting, enhance visual quality, and unlock new possibilities in their projects.



