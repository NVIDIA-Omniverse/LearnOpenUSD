# Attributes

USD attributes are one of the two types of USD properties, the other being relationships. Properties are used to describe the characteristics of objects, or "prims," within a USD scene.

Attributes store data values that define the appearance, behavior, or other properties of a prim.

Relationships, on the other hand, establish connections between prims, enabling hierarchical structures and data sharing.

For this lesson, we'll concentrate on attributes.

<@ nvfunc kaltura 1_u0uzffig @>

Attributes are the most common type of property that you'll work with when creating scenes. An attribute can have one specific data type, such as a number, text, or a vector. Each attribute can have a default value, and it can
also have different values at different points in time, called timeSamples.

### How Does It Work?

Attributes are name-value pairs (often referred to as key-value pairs) that store data associated with a prim.

Any given attribute has a single, defined data type associated with it. Each attribute is defined with the type of data that it can hold. A single attribute can represent various types of properties, such as the vertices of a piece of geometry, the diffuse color of a material, or the mass of an object. These are typically defined through the `Sdf` library.

Some common examples of attributes include:

* **Visibility** - Controls the visibility of a prim in the scene.
* **Display color** - Specifies the display color applied to a geometric prim.
* **Extent** - Defines the boundaries of a geometric prim. 

Attributes can be authored and stored within USD layers, which are files that describe different aspects of a scene. When a USD stage is composed, the attribute values from various layers are combined according to specific
composition rules, allowing for flexible scene assembly.

Attributes can be animated by providing multiple key-framed values over time. OpenUSD's timeSampling model ensures efficient storage and interpretation of animated data.

### Working With Python

To work with attributes in OpenUSD, we will generally use schema-specific APIs. Each schema-specific API has a function to grab its own attributes. Review the following examples to learn more.

```python
# Get the radius value of sphere_prim that is of type UsdGeom.Sphere
sphere_prim.GetRadiusAttr().Get()

# Set the double-sided property of the prim
sphere_prim.GetDoubleSidedAttr().Set(True)
```

While there’s also a dedicated `UsdAttribute` API, in general, it's preferred to use the schema-specific methods, if they exist, as they are more clear and
less brittle. You can learn more about how to work with each specific schema on OpenUSD’s [documentation](https://openusd.org/release/api/annotated.html).

### Key Takeaways

In summary,

* Attributes are values with a name and data type that define the properties of prims in a USD scene. 
* Attributes are the primary means of storing data in USD. 
* Each attribute has a single, defined data type.
* Attributes are authored and stored within USD layers, enabling efficient scene composition.
* Attributes can be animated by providing key-framed values over time.
* They can be queried, modified and animated using the USD API.

Understanding attributes is essential for creating rich and detailed 3D scenes, enabling efficient collaboration and interoperability across various tools and pipelines.

In the next lesson, let's talk about the other USD property: relationships.



