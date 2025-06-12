# Primvars 

Primvars enable efficient management and manipulation of hierarchical object data in complex 3D scenes. Continue on with this lesson to learn more.

```{kaltura} 1_pqmuz40u
```

Short for primitive variables, primvars are special attributes that contain extra features. They address the following problems in computer graphics:

* The need to "bind" user data on geometric primitives that becomes available to shaders during rendering.
* The need to specify a set of values associated with vertices or faces of a primitive that will interpolate across the primitive's surface under subdivision or shading.
* The need to inherit attributes down namespace to allow sparse authoring of shareable data.

Some examples include, texture coordinates, vertex colors, or custom metadata, allowing for interpolating data on individual objects.

Primvars are essential for various tasks, including:

* Storing UVs for texture mapping
* Defining vertex colors for per-Vertex shading
* Deformation and animation



### How Does It Work?

Primvars are defined within the scene description and can be accessed and modified using OpenUSD APIs. Each primvar can store different types of data, such as scalar values, vectors, or arrays.

### Working With Python

Developers working with OpenUSD can interact with primvars using the Python API.

```python
# Constructs a UsdGeomPrimvarsAPI on UsdPrim prim
primvar_api = UsdGeom.PrimvarsAPI(prim)

# Creates a new primvar called displayColor of type Color3f[]
primvar_api.CreatePrimvar('displayColor', Sdf.ValueTypeNames.Color3fArray)

# Gets the displayColor primvar
primvar = primvar_api.GetPrimvar('displayColor')

# Sets displayColor values
primvar.Set([Gf.Vec3f(0.0, 1.0, 0.0)])

# Gets displayColor values
values = primvar.Get()
```

### Key Takeaways

The ability to store and manipulate hierarchical object data using primvars is a powerful feature that enables advanced 3D workflows and facilitates interoperability between different tools and applications. By leveraging
primvars effectively, we’ll be able to efficiently manage and manipulate per-object data in complex 3D scenes, enabling advanced workflows and facilitating interoperability between different tools and applications.



