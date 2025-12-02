# OpenUSD Instancing Frequently Asked Questions

## What are the differences between Scenegraph Instancing and Point Instancing?

**Scenegraph Instancing**
* {term}`Composition <Composition>`-based instancing
* Implicit prototypes derived from {term}`composition arcs <Composition Arcs>`
* Instance and instance descendants identifiable via {term}`path <Path>`
* Each instance has an instanceable prim that's editable, but the subgraph--instance proxy--is read-only
* Transparent deinstancing
* Good for reusing complex components (e.g. shelf assemblies, robots)

**Point Instancing**
* {term}`Schema <Schema>`-based instancing
* Explicit prototypes specified in scene description
* Instances identifiable via index
* Invasive deinstancing
* May be combined with scenegraph instancing
* Good for massive numbers of simpler items where the overhead of an instance outweights the benefits of reuse. (e.g. leaves on trees)