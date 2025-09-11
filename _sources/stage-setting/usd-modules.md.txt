# OpenUSD Modules

In this lesson, we're talking about a few commonly used USD modules that are a great place to start for OpenUSD development. 

## What Are the Core USD Modules?
The USD code repository is made up of four core packages: `base`, `usd`, `imaging`, and `usdImaging`. To author and read USD data, you only need the `base `and `usd` packages. We will focus on modules found in these two packages.

```{kaltura} 1_n2oh1grs
```

USD’s API consists of many modules with varying purposes including: authoring, reading, and composing USD data, imaging composed scenes, defining plugin interfaces for extending USD’s capabilities, and more.

### How Does It Work?

When authoring or querying USD data, you will almost always use a few common USD modules such as `Usd`, `Sdf`, and `Gf` along with some schema modules. Schemas are grouped into schema domains and each domain has its own module. The schema modules you use will depend on the type of scene description you’re working with. For example, `UsdGeom` for geometry data, `UsdShade` for materials and shaders, and `UsdPhysics` for physics scene description.

### Working With Python

The schema modules are covered more in depth in relevant videos for each domain. Let’s have a closer look at a few of the other common USD modules: `Usd`, `Sdf`, and `Gf`. In Python, you can import these modules from the `pxr`
namespace:

```python
# Import Usd, Sdf, and Gf libraries from Pixar
from pxr import Usd, Sdf, Gf
```

`Usd` is the core client-facing module for authoring, composing and reading USD. It provides an interface for creating or opening a Stage and generic interfaces for interacting with prims, properties, metadata, and composition arcs.

`Sdf` (scene description foundation) provides the foundations for serializing scene description to a reference text-based file format and implements scene
description layers, (`SdfLayer`) which stores part of the scene description. Most notably, you will commonly see this module used for managing prim and property paths and creating USD layers.

`Gf` is the graphics foundation and contains the foundation classes and functions that contribute graphics, like Linear Algebra, Basic Mathematical Operations and Basic Geometry. This module contains classes for 3D data types that you will use for getting and setting particular USD attributes.

## Key Takeaways

Now, you should be more familiar with the commonly used  USD modules for OpenUSD development to start exploring the OpenUSD API on your own. You can find the full set of core packages and modules available to you on {usdcpp}`OpenUSD.org <index>`.



