# What Is Asset Modularity?

![](../../images/asset-modularity-instancing/slides/Slide13.jpg)

Let’s give a quick refresher on Composition Arcs and Layer Stacks.​

In OpenUSD, a scene is composed through its root layer stack.  That's the root layer plus all sub layers, including sub layers of sub layers. 

## Composition Arcs

Here we have a scenario.usd which is broken down into facility.usd and elements.usd sublayers.​

![](../../images/asset-modularity-instancing/slides/Slide14.jpg)

​Composition arcs are used to compose data from other layer stacks into the root one.​

The facility sublayer is using composition arcs to compose a warehouse onto the Usd Stage.  The storage sublayer is composing racks onto the Usd stage.​
​
Together OpenUSD composition arcs and layer stacks are the fundamental mechanisms that enable the creation and management of complex 3D scenes.​

When learning OpenUSD, we don't always distinguish between layer stacks and arcs. They're often grouped together as "composition operators".  Distinguishing the operations becomes important when understanding advanced topics, as behaviors sometimes depend on this distinction.​

Instancing is one of those cases where this difference matters, which is why we’re highlighting this.

![](../../images/asset-modularity-instancing/slides/Slide15.jpg)

Composition adheres to a specific strength ordering, known as LIVERPS (Local, Inherits, VariantSets, Relocates, References, Payloads, Specializes), which determines how conflicts are resolved when multiple opinions exist for the same data. Local here refers to the "local layer stack".  This system ensures a predictable and controlled outcome when composing disparate scene data.

## Asset Modularity

![](../../images/asset-modularity-instancing/slides/Slide16.gif)

Okay, now that we’ve refreshed composition, let’s dive into our first topic modularity.​

Modularity is the principle of building complex systems from smaller, self-contained components, called modules or assets.​

Composition is foundational to the construction of modular scenes.​

* In the context of OpenUSD, composition makes it possible to:​
* Decompose a project into manageable parts​
* Iterate on those parts independently​
* Synthesize those parts into a larger scene​
* Reuse components across multiple projects​

Let’s look at an example.

![](../../images/asset-modularity-instancing/slides/Slide17.jpg)

One team might be responsible for designing a rack, another team might be responsible for laying out the racks in a warehouse, and yet another team responsible for simulating various scenarios in the warehouse.

There are several benefits to reusing content - 
* *Validation and Standardization*: Less redundancy means less opportunity for errors. assets that are reused improve navigability and legibility simply through users becoming familiar with the underlying asset structure.
* *Efficiency* through Centralized editing: Change the underlying asset once, and all uses are instantly updated.
* *System Performance*: If you’re running dozens of scenarios and they all use the same robot and factory, the scenarios benefit from sharing of system resources.  The precise benefits will vary depending on your system, asset resolver, and file format, but the benefits will be scoped to the cost of layer operations.

![](../../images/asset-modularity-instancing/slides/Slide18.jpg)

Modularity within a project is great, but it can be extended across projects with through object catalogs and libraries.  An asset library can share multiple parts to facilitate reuse among several assets. Pallets could be used as individual components, or as part of an aggregate asset like box_palette or box_palette_rack.  The same layer gets used in both.

Asset libraries form the backbone of large environments (like factories or supply chains) by grouping related modules.

In software development, you may be familiar with the DRY principle - Don’t Repeat Yourself. In USD, this means:
Avoid duplicating the same object or data.
Reference an existing, central asset whenever possible.

With OpenUSD a scene can be synthesized from multiple libraries with different asset structures, different pipelines, and different toolsets. You might get your architecture from an internal CAD tool and digital humans from a third party asset package.  Different modular asset structures can coexist within the same composed stage.

![](../../images/asset-modularity-instancing/slides/Slide19.jpg)

Modularity and Reuse provide both workflows advantages and technical gains.

Workflow advantages:
* Parallelize workstreams so that different teams work on assets that are shared amongst multiple scenarios.
* Importantly, different teams may use different tools or catalogs.
* Easier to update or swap out defective pieces.
* Easier to test design iterations in context

Technical gains:
* Reduces the number of layers that needs to be accessed or opened by your filesystem or network
* Reduces file size, RAM, and VRAM use (important for both simulation and rendering).
