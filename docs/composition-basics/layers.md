# Layers

## What Are Layers?
![](../images/foundations/layer_Definition.webm)

OpenUSD scenes are organized into {term}`layers <Layer>`, whose contents can be combined or overridden to create a composed scene, with each layer containing a subset of the complete scene data (such as geometry, materials, or animations).

This layered approach allows for non-destructive editing, where changes made to one layer do not affect the others. Layers can be thought of as modular pieces that, when composed together, form a complete scene.

A layer is a single file or resource that contains scene description data. This could be a USD file (.usd, .usda, .usdc), a file format supported by a plugin (e.g. .gltf, .fbx, etc.) or even a resource that’s not file-based at all (e.g. from a database).

Each USD {term}`stage <Stage>` is made of {term}`layer stacks <Layer Stack>` composed at runtime to represent a
scene.

![A diagram depicting independent layers building up to an aggregate scene.](../images/foundations/Layers.png)


### How Does It Work?

The true power of layers lies in their ability to be composed together into a single, coherent scene. While it is easy to think of USD layers similar to the concept of Photoshop layers, we avoid that analogy, as it only covers sublayering, which is only one of many USD {term}`composition arcs <Composition Arcs>`.

![diagram representing sublayers](../images/foundations/Sublayers.png)

---

![](../images/foundations/layer_USDvsPhotoshop.webm)

While Photoshop composes its final product by compiling each layer on top of the one below it, USD's composition engine combines the data across composition arcs according to a specific {term}`strength ordering <LIVERPS Strength Ordering>`, resolving conflicts based on the arcs’ relative strengths. This strength ordering is referred to as LIVRPS (pronounced "liver peas") – an acronym we'll explain in later lessons.

There are a few practical ways we leverage layers in OpenUSD for collaborative and non-destructive workflows. Layers are used for:

* Separating scene data by discipline for parallel and modular workstreams.
* Creating reusable asset libraries that can be referenced across multiple scenes.
* Enabling collaborative workflows where different teams or artists can work on separate layers concurrently.
* Structuring scene data for efficient loading and {term}`instancing <Instancing>` (such as using {term}`payloads <Payload>` or {term}`references <Reference>`).
* Non-destructive editing by introducing new layers for changes.

### Working With Python

![Python examples for Layers](../images/foundations/layer_Python.webm)

The following are common functions we use when interacting with layers in USD.

* `layer.Reload()` - Clears all content/opinions not saved on that layer
* `layer.Save()` - Saves content from that layer to disk


## Key Takeaways

Layers are a fundamental concept in USD, enabling modular scene description, efficient collaboration, and non-destructive editing. Understanding how layers are composed and their strength ordering is important for effectively working with USD scenes.

In the next lesson, we will explore the concept of strength ordering, which provides the rules that govern how layers are combined and how conflicts are resolved.



