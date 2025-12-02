# What Is Instancing?

Understanding instancing is the key to building large, efficient scenes, like what’s required for digital twins. Instancing may be familiar to you from other applications or contexts. In this lesson, we present the concept of instancing at a high-level to serve as a common foundation.

This foundation will be helpful for later lessons where we will breakdown OpenUSD's specific instancing implementations: scenegraph instancing and point instancing.

## Where Instancing Comes In

![](../images/asset-modularity-instancing/layer-stacks-composition-arcs.png)

We started the module refreshing the concepts of composition in OpenUSD. We have our local layer stack and then our composition arcs that compose content into the local layer stack.

![](../images/asset-modularity-instancing/sparse-overrides.gif)

The local layer stack functions as the point of refinement for all the content you've composed. Robots can be articulated and assembly lines simulated. Materials can be modified, {term}`variants <Variant>` can be selected.

Sparse {term}`overrides <Over>` are often referred to as OpenUSD's superpower. You can work modularly, assemble, and continue to refine downstream.

Encapsulating your {term}`assets <Asset>` in modular {term}`layers <Layer>` facilitates data reuse. Reuse amortizes the cost of a layer both within a scene and across scenes. We get a lot of flexibility that supports unique overrides. Post composition, runtimes may be able to detect whether {term}`attribute <Attribute>` values or parts are the same as a form of data deduplication.

```{figure} ../images/asset-modularity-instancing/just-composition.png 

Using composition to repeat an asset and refining the copies with unique overrides.
```

But data deduplication isn't free. You're trading time and algorithmic complexity for in-memory scene size. We have to go through the scene and check each individual robot arm is the same as the source or not. Has it been refined? Does it have overrides?

It would be nice to be able to say up front that a particular scene element is not open to refinement. This is instancing. 

```{figure} ../images/asset-modularity-instancing/composition-and-instancing.png

Composition with instancing saves processing time.
```

Instancing is a declarative deduplication of modular repetition. We're going to say we're going to limit our per instance customizations and share the composed result among the copies to create a fast and memory efficient view of the scene.

We can save scene graph processors lots of time by declaratively tagging parts of our scene as being not open to editing downstream.


::::{grid} auto

:::{grid-item} 
:columns: 6
:child-align: center

```{figure} ../images/asset-modularity-instancing/dedup-before.png
Before deduplication
```
:::
:::{grid-item} 
:columns: 6

```{figure} ../images/asset-modularity-instancing/dedup-after.png
After deduplication
```
:::

::::

## Key Takeaways

Modularity and content reuse is enabled by sharing data through layers. We can deduplicate repeated modularity to reduce runtime resource usage.

Instancing accelerates the performance of deduplication. You *could* go through and check each individual robot to see if each robot is identical at runtime. Instead, instancing gives you a shortcut to say, yeah, yeah, we know these are identical. We didn't put any overrides on this. This allows you to simplify the view of your scene and reducing the work to deduplicate.

In the next lessons we will learn about the two instancing implementations in OpenUSD: scenegraph instancing and point instancing.