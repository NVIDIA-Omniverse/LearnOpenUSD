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
# Default Prim
![Default Prim Definition](../images/DefaultPrim_Definition.webm)

In this lesson, we’ll explore the concept of default prims in Universal Scene Description. Default prims are essential for scene management, especially when dealing with complex hierarchies and references. By the end of this lesson, we’ll understand what default prims are, why they are important, and how to set them using Python.

### How Does It Work?

A default prim in OpenUSD is a top-level prim, or primitive, that is part of the scene’s metadata and serves as the primary entry point or root for a stage. Think of it as the “control point” in the scene, which helps other parts of the system know where to start or what to focus on.

It is best practice to set a default prim in our stages. This is crucial for tools and applications that read USD files, as it guides them to the primary content; for some it may even be considered invalid if the default prim is not specified for the stage. `usdchecker` checks for a default prim and reports an
error if it is not set on a stage. A default prim is also particularly useful when the stage’s root layer is referenced in other stages (such as a reference or payload), as it eliminates the need for consumers to specify a target prim manually.

Let’s look at this example. Let's assume we have a USD file named
`simple_scene.usda` with the following content:
```usda
#usda 1.0
(
    defaultPrim = "Car"
)

def Xform "Car" {
    def Mesh "Body" {
        double3[] points = [(0, 0, 0), (2, 0, 0), (2, 1, 0), (0, 1, 0)]
        int[] faceVertexCounts = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]
    }
}

def Xform "Building" {
    def Mesh "Structure" {
        double3[] points = [(0, 0, 0), (5, 0, 0), (5, 10, 0), (0, 10, 0)]
        int[] faceVertexCounts = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]
    }
}
```

The `defaultPrim` metadata is set to `Car`, indicating that `Car` is the main entry point of this USD file. When we bring this `.usda` in as a reference or payload the `Car` will show up visually in the stage. If we set the `defaultPrim` to `Building` then the `Building` will show up in the stage when referenced. If no `defaultPrim` is set then when the above `.usda` is brought
in as a payload or reference it will resolve as an empty layer and output a warning message in the log.

### Working With Python

![Default Prim Python](../images/DefaultPrim_Python.webm)

The default prim is set using the `SetDefaultPrim()` method on a USD stage. This method accepts any `Usd.Prim`, but the prim must be a top-level prim on the stage. Here’s a simple example:

```python
from pxr import Usd, UsdGeom, Sdf

# Create a new USD stage
stage = Usd.Stage.CreateInMemory()

# Define a top-level Xform prim
default_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()

# Set the Xform prim as the default prim
stage.SetDefaultPrim(default_prim)

# Export the stage to a string to verify
usda = stage.GetRootLayer().ExportToString()
print(usda)

# Check that the expected default prim was set
assert stage.GetDefaultPrim() == default_prim
```

## Examples

### Example 1: Setting a Default Prim

[`SetDefaultPrim()`](https://openusd.org/release/api/class_usd_stage.html#a82b260faf91fbf721b0503075f2861e2) sets the default prim for the stage's root layer.

A `Default Prim` is layer metadata. If the stage's root layer is used as a [`Reference`](https://openusd.org/release/glossary.html#usdglossary-references) or [`Payload`](https://openusd.org/release/glossary.html#usdglossary-payload) it is best practice to set a Default Prim.

**Add the following code to the cell below, then run the cell:**

```python
# Set the default primitive of the stage to the primitive at "/hello":
stage.SetDefaultPrim(hello_prim)
```

```{code-cell} ipython3
:cell_id: fbe74dc41642445493344df4a7aaef8d
:deepnote_cell_type: code
:id: Nta3XsuHNDbN

from pxr import Usd

stage: Usd.Stage = Usd.Stage.Open("assets/prims.usda")
stage.DefinePrim("/hello")
stage.DefinePrim("/hello/world")
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")
world_prim: Usd.Prim = stage.GetPrimAtPath("/world")

print(hello_prim.IsValid())
print(world_prim.IsValid())

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
print(stage.ExportToString())
```

### Key Takeaways

In summary, default prims are the top-level prims that serve as the main entry point for a USD stage. Setting a default prim is a best practice when our stage’s root layer might be composed into another stage, whether as a reference, payload, or specialize.

By utilizing default prims, we can create more organized and manageable USD stages.



