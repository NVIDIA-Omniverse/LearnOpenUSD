`XformCommonAPI ` is a component of the OpenUSD framework. Today, we're diving into this API to understand its utility in the 3D content creation pipeline.

This API facilitates the authoring and retrieval of a common set of operations with a single translation, rotation, scale and pivot that is generally compatible with import and export into many tools. It's designed to simplify the interchange of these transformations.

<@ nvfunc kaltura 1_tx9y8k5c @>

### How Does It Work?

The API provides methods to get and set these transformations at specific times--for instance, it allows the retrieval of transformation vectors at any
given frame or TimeCode, ensuring precise control over the simulation process.

There’s another way to author and retrieve translations – through the `UsdGeomXformable` function. Xformable prims support arbitrary sequences of transformations, which gives power users a lot of flexibility. A user could
place two rotations on a “Planet” prim, allowing them to control revolution and rotation around two different pivots on the same prim. This is powerful, but complicates simple queries like “What is the position of an object at time 101.0?”

### Working With Python

Below is an example of how to work with the `XformCommonAPI` in a USD environment.

```python
from pxr import Usd, UsdGeom

# Create a stage and define a prim path
stage = Usd.Stage.CreateNew('example.usda')
prim = UsdGeom.Xform.Define(stage,'/ExamplePrim')

# Check if the XformCommonAPI is compatible with the prim using the bool operator 
if not (xform_api := UsdGeom.XformCommonAPI(prim)):
    raise Exception("Prim not compatible with XformCommonAPI")
```

These commands demonstrate how to apply translations, rotations, and scaling to a 3D object using the `XformCommonAPI`. We can get a transformation matrix
from the xformable prim that works with any `xformOp` order using the [`GetLocalTransformation`](https://openusd.org/release/api/class_usd_geom_xformable.html#a9a04ccb1ba8aa16e8cc1e878c2c92969) method.

### Key Takeaways

The `XformCommonAPI` provides the preferred way for authoring and retrieving a standard set of component transformations, including scale, rotation, scale-
rotate pivot and translation.

The goal of the API is to enhance, reconfigure or adapt each structure without changing the entire system. This approach allows for flexibility and customization by focusing on the individual parts rather than the whole. This is done by limiting the set of allowed basic operations and by specifying the order in which they are applied.
