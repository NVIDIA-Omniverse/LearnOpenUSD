# Nested Instancing

## What Is Nested Instancing?
Nested instancing is when an instance subgraph has instances within it. Nested instancing can unlock even more performance optimizations.

Common patterns:
* Instanced assemblies with instanced components.
* Instanced components with instanced material networks.

Nesting instancing is not limited to scenegraph instances only. You can include PointInstancers within a scenegraph instance and vice versa. We will explore PointInstancers in the [point instancing lesson](../authoring-point-instancing/index.md).

Be cautious about introducing too much complexity with your nested instancing schemes.

## Assemblies

Assemblies in OpenUSD create a good opportunity to utilize nested instancing.

```{figure} ../../images/asset-modularity-instancing/nested-instancing.mp4
Assembly prototypes that encompass nested prototypes.
```

Here we have our factory on the left hand side of the screen. It's constructed from the robot, shelf, pallet, and box assets.

If you notice the the pallets appear six times and the racks with pallets appear two times. There's actually an opportunity to create aggregate assets: pallet with boxes and the fully assembled racks. Best of all, we can instance those as well.

We can instance the assemblies and then their contents can also contain instances. Nested instancing like this enables large-scale scene aggregation.

## Material Networks

Material networks can be a really good point for instancing as well. Sometimes your material networks within your assets are more complicated than the geometry in terms of number of prims. 

It's common to reference a material network from a library. If you're referencing it, you can instance it.

When a component asset using an instanced material network is instanced, guess what? You have nested instancing.



