# Metadata


## What is Metadata?
![Metadata Definition](../images/Metadata_Definition.webm)

Metadata in OpenUSD refers to a set of name-value pairs that provide additional, non-animatable information attached to prims or their properties. The concept is similar to properties, but it allows us to add custom information or annotations to scene description elements via a dictionary without modifying the underlying schema or data model.

### How Does It Work?

![Metadata Use case](../images/Metadata_UseCase.webm)

Metadata is stored separately from the primary data and can be accessed and modified independently. It is typically used to store additional information that is not directly related to the geometry or rendering of an object, such as:

* Author information
* Creation/modification dates
* Project-specific data
* Annotations or notes
* Rendering hints or flags

Metadata can be set at different levels of the scene hierarchy, allowing for both global and localized metadata.

![Metadata vs Attributes](../images/Metadata_vsAttributes.webm)

While both metadata and attributes allow us to store additional data, there are some key differences:

* Metadata is separate from the core schema and data model, while attributes are part of the schema definition.
* Metadata is typically used for supplementary information, while attributes are often used for data directly related to the object's properties or behavior.
* Metadata cannot be sampled over time (i.e. timesamples), allowing it to be evaluated and stored more efficiently than attribute values.

### Working With Python

![Metadata Python](../images/Metadata_Python.webm)

Here are a few ways we can interact with metadata via the Python API:

```python
# Retrieve the metadata value associated with the given key for a USD Object
usdobject.GetMetadata('key')

# Set the metadata value for the given key on a USD Object
usdobject.SetMetadata('key', value)

# Retrieve the metadata value associated with the given key for the stage
stage.GetMetadata('key')

# Set the metadata value for the given key on the stage
stage.SetMetadata('key', value) 

# Use for better performance if accessing a single value and not all the metadata within a key
GetMetadataByDictKey()
```

It’s worth noting that `key` will typically be either `assetInfo`, which can be used to set asset related data or `customData`, which can be used for everything else. We can only create custom metadata keys by adding a new schema.

## Key Takeaways

The metadata API in OpenUSD provides a flexible way to store and access additional information about prims and attributes through a dictionary, without modifying the core schema or data model. While metadata and custom attributes serve different purposes, understanding their differences and appropriate use cases is essential for effective scene description and data management in OpenUSD.



