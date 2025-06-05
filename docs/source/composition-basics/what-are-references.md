This lesson talks briefly about references. The word may seem familiar – we introduced the concept in the previous lesson on strength ordering, where “references” represents the R in LIVRPS.

References in Universal Scene Description are a composition arc that enable the composition of prims and their descendants onto other prims – this allows us to use references to aggregate larger scenes from smaller units of scene description. This can be done with external references, which load data from other files, or internal references, which load data from other parts of the hierarchy.

They are fundamental in USD's composition system, enabling modular and
reusable scene description, and they are the second most important composition arc in USD, after sublayers.

![](../../images/References_Definition.webm)

### How Does It Work?

A reference statement includes the address of the layer to reference from
(which can be omitted for internal references) and the prim path to reference (which can be omitted if you want to load an entire external layer which has a default prim defined).

When a prim is composed via a reference arc, USD first composes the layer
stack of the referenced prim, then adds the resulting prim spec to the
destination prim. Then, it applies any overrides or additional composition arcs from the destination prim.

### Working With Python

![References Python](../../images/References_Python.webm)

Here are a few ways you can work with references using the Python API:

```python
# Return a UsdReferences object for managing references on a prim
prim.GetReferences()

# Add a reference to the specified asset and prim path
references.AddReference(assetPath, primPath) 

# Remove all references from a prim
references.ClearReferences()
```

### Key Takeaways

So, why is it important to understand and leverage references properly?
References have several practical use cases.

As mentioned earlier, references are also useful for building large, complex scenes by referencing smaller sub-scenes or components.

We see referencing used commonly for asset libraries, where you might have assets, materials or other props reused across several scenes.

By leveraging references, artists and developers can create more efficient workflows, manage complex scenes, and collaborate more effectively across different departments and production stages. Let's get into a few examples to better understand how we can use references in our workflows.

