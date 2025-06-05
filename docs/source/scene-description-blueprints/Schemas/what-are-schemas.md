![Schema Definition](../../images/Schema_Definition.webm)

Schemas give meaning to prims in OpenUSD, i.e., “What is this element? What capabilities does it have?”. Schemas define the data models and optional API for encoding and interchanging 3D and non-3D concepts through OpenUSD.

In the next couple lessons on schemas, we'll explore the different types of schemas, their characteristics, and how they enable the creation of sophisticated virtual worlds and digital twins.



### What Are Schemas?

Schemas serve as blueprints that author and retrieve data, like attributes and relationships that govern behaviors of elements in a USD scene. They provide a consistent and extensible way to define and interpret data, ensuring data interoperability between different software tools and applications.

Each prim in a scene is an element that implicitly contains the properties and fallback values of the typed schema that’s telling the prim what it is. For example, the `radius` attribute for the `UsdGeomSphere` schema is defined as `double radius = 1` meaning that all sphere prims have a radius represented by a double-precision floating point number with a value of `1` by default.

Schemas are primarily data models with documented rules on how the data should be interpreted. While schemas define the structure and rules, they do not necessarily include the implementation of behaviors. For example, the `UsdPhysics` schema does not come with a physics engine. Developers should understand that schemas often expose methods to facilitate interactions with
the defined structure and may provide behaviors in the schema API, but this is not a requirement.

There is a trend toward codeless schemas for easier distribution, suggesting that schemas might become more lightweight, focusing on data modeling rather than behavior implementation.

Actual behavior enforcement can be managed by other subsystems within the runtime ecosystem. This allows for flexibility and performance optimization based on different use cases.



### Working With Python

![Schema Python](../../images/Schema_Main.webm)

In Python, we can work with schemas using the following methods:

```python
# Retrieve the schema info for a registered schema
Usd.SchemaRegistry.FindSchemaInfo()

# Retrieve the schema typeName
Usd.SchemaRegistry.GetSchemaTypeName()
```

These methods allow us to interact with and manipulate schemas
programmatically, enabling us to create, modify, and validate USD assets based on predefined rules and conventions.



### Key Takeaways

Schemas in OpenUSD serve as templates for defining prims.

It's worth noting there are actually two distinct types of schemas: IsA and API schemas, which we'll cover in the next lesson.



