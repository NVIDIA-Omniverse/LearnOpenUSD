# Relationships

In the previous lesson, we introduced the concept of USD properties, which are used to describe the characteristics of prims in USD scenes. As mentioned, there are two types of USD properties: attributes and relationships. This
lesson will discuss relationships.

Relationships establish connections between prims, acting as pointers or links between objects in the scene hierarchy. A relationship allows a prim to target
or reference other prims, attributes, or even other relationships. This establishes dependencies between scenegraph objects.

<@ nvfunc kaltura 1_3tz14vzm @>

### How Does It Work?

Relationships store path values that point to other scene elements. When you query a relationship's targets, OpenUSD performs path translations to map the authored target paths to the corresponding objects in the composed scene
prims.

Relationships are robust against path translations, a key advantage over hard-coded paths. If a target prim's path changes due to editing or referencing, the relationship automatically remaps to the new location.

Relationships can have multiple targets, making them useful for grouping or collecting objects together. For example, a material relationship might target all geometry prims that should use that material.

Note that a relationship is an alternative type of property to an attribute. Unlike an attribute, it has no data type. It is a way of declaring, at creation time, that the only use for a property is to record linkage
information. Conceptually, it is like an attribute whose data type is a "link". This means you can _not_ use a relationship to connect two already-existing attributes--for that, you can use attribute connections.

### Working With Python

Here are a few Python commands to familiarize yourself as you work with relationships. These can be useful as you establish connections between different scene elements, like materials and geometry.

```python
# Get the target paths of a relationship
UsdRelationship.GetTargets()

# Set the target paths for a relationship
UsdRelationship.SetTargets()

# Add a new target path to a relationship
UsdRelationship.AddTarget()

# Remove a target path from a relationship
UsdRelationship.RemoveTarget()
```

### Key Takeaways

Relationships enable robust encoding of dependencies and associations between scene elements, such as:

* Binding geometry to materials
* Grouping prims into collections
* Establishing connections in shading networks
* Modeling hierarchical relationships (e.g. parent-child)

Using relationships instead of hard paths enhances:

* Non-destructive editing workflows
* Referencing and asset reuse across tools
* Collaborative workflows across teams

Relationships are a way to link scene elements while enabling non-destructive editing and cross-tool collaboration. They enhance the flexibility and scalability of OpenUSD-based pipelines.



