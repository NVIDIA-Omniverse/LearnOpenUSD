# What is Point Instancing?

![](../../images/asset-modularity-instancing/slides/Slide47.jpg)

Scenegraph Instancing:
* What we've been talking about is scene graph instancing
* Good for reusing complex components (like full shelf assemblies, robots).
* Instances are part of the readable scenegraph; each has a "root prim” that’s editable, but the subgraph is read-only.
Point Instancing:
* Designed for massive numbers of simpler items where the overhead of an instance outweights the benefits of reuse.
* Example: a tree with 100,000 leaves
* Even more efficient, but you lose some ability to edit each instance individually.
