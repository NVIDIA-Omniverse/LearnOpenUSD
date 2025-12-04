# What Is Asset Modularity?

This lesson is going to focus on modularity and content reuse in OpenUSD. We'll talk about how USD enables modern content pipelines to be more efficient, flexible, and scalable by embracing these principles.

## Review: Layer Stacks and Composition Arcs

![](../../images/asset-modularity-instancing/root-layer-stack.png)

We will briefly refresh on {term}`composition arcs <Composition Arcs>` and {term}`layer stacks <Layer Stack>` here. 

```{seealso}
The [Creating Composition Arcs](../../creating-composition-arcs/index.md) module covers layer stacks and composition arcs in-depth and we recommend starting there if you haven't gone through it. 
```

In OpenUSD, a scene is composed through its {term}`root layer stack <Root Layer Stack>`.  That's the root {term}`layer <Layer>` plus all {term}`sublayers <Sublayer>`, including sublayers of sublayers.

Here we have a "scenario.usd" which is broken down into facility.usd and "elements.usd" sublayers.​ Composition arcs are used to compose data from other layer stacks into the root one.

![](../../images/asset-modularity-instancing/layer-stacks-composition-arcs.mp4)

The facility sublayer is using composition arcs to compose a warehouse onto the USD {term}`stage <Stage>`. The elements sublayer is composing various {term}`references <Reference>` of the rack {term}`asset <Asset>` onto the stage.​

Together, OpenUSD composition arcs and layer stacks are the fundamental mechanisms that enable the creation and management of complex 3D scenes.​

When learning OpenUSD, we don't always distinguish between layer stacks and arcs. They're often grouped together as composition operators.  Distinguishing the operations becomes important when trying to develop advanced understanding of topics like instancing, as basically the behavior of instancing depends on this distinction.

![](../../images/asset-modularity-instancing/liverps-strength-ordering.png)

{term}`Composition <Composition>` adheres to a {term}`strength ordering <LIVERPS Strength Ordering>`, known as LIVERPS--Local, Inherits, Variant Sets, Relocates, References, Payloads, and Specializes. This ordering determines how conflicts are resolved when multiple {term}`opinions <Opinions>` exist for the same data. Local here refers to the local layer stack.

This system ensures a predictable and controlled outcome when composing disparate scene data.

## Asset Modularity and Content Reuse

![](../../images/asset-modularity-instancing/modularity.gif)

Now that we’ve refreshed composition, let’s dive into our first topic, modularity.​

Modularity is the principle of building complex systems from smaller, self-contained components, called modules or assets.​

Composition is foundational to the construction of modular scenes.​

In the context of OpenUSD, composition makes it possible to:​
* Decompose a project into manageable parts​
* Iterate on those parts independently​
* Synthesize those parts into a larger scene​
* Reuse components across multiple projects​

### Standardization, Efficiency, and Performance Benefits

Let’s look at an example.

![](../../images/asset-modularity-instancing/content-reuse.png)

One team might be responsible for designing a rack, another team might be responsible for laying out the racks in a warehouse, and yet another team responsible for simulating various scenarios in the warehouse.

There are several benefits to structuring our assets so that we can reuse content.

**Validation and Standardization**

Less redundancy means less opportunity for errors. The rack in scenario one is the same rack in scenario three and scenario four. If it's been validated for scenario one, there's a good chance that it will also work well in scenario three and four.

In terms of standardization, assets that are reused improve navigability and legibility simply through users becoming familiar with the underlying asset structure.

**Efficiency Through Centralized Editing**

If you change the underlying asset once, all uses are instantly updated. If we needed to add a new {term}`variant <Variant>` to the rack, or change the material to a more advanced material model, we can do that and then have it propagate through the warehouse all the way back up to our scenarios.

**System Performance**

There is a system performance benefit to this--it's not just workflow improvements. If you’re running dozens of scenarios and they all use the same robot and factory, the scenarios benefit from sharing of system resources like storage and memory. The precise benefits will vary depending on your system, asset resolver, and file format, but the benefits will be scoped to the cost of layer operations.

### Enabling Asset Catalogs and Libraries

![](../../images/asset-modularity-instancing/asset-library.png)

Modularity within a project is great, but it can be extended across projects through object catalogs and libraries. An asset library can share multiple parts to facilitate reuse among several assets. Pallets could be used as individual components, or as part of an aggregate asset like "box_pallet.usd" or "box_pallet_rack.usd".  The same layer gets used in both.

Asset libraries form the backbone of large environments (like factories or supply chains) by grouping related modules.

In software development, you may be familiar with the DRY principle--Don’t Repeat Yourself. In USD, this means:

* Avoid duplicating the same object or data.
* Reference an existing, central asset whenever possible.

With OpenUSD, a scene can be synthesized from multiple libraries with different asset structures, different pipelines, and different toolsets. You might get your architecture from an internal CAD tool and digital humans from a third party asset package.

Different modular asset structures can coexist within the same composed stage.

## Why Does It Matter?
![](../../images/asset-modularity-instancing/why-it-matters.png)

Modularity and content reuse provide both workflows advantages and technical gains.

**Workflow Advantages**

* Parallelize workstreams so that different teams work on assets that are shared amongst multiple scenarios.
* Different teams may use different tools or catalogs.
* Easier to update or swap out defective pieces.
* Easier to test design iterations in context

**Technical Gains**

* Reduces the number of layers that needs to be accessed or opened by your filesystem or network
* Reduces file size, RAM, and VRAM use (important for both simulation and rendering).
