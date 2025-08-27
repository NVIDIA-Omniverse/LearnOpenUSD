# What Is Instancing?

Great, let’s move onto the next lesson: What Is Instancing?
Understanding instancing is the key to building large, efficient scenes, like what’s required for digital twins. 

* Brief overview of Scenegraph Instancing?
* Why it matters?
* What are the benefits?

## Composition Arcs Refresher

![](../../images/asset-modularity-instancing/slides/Slide23.jpg)

We started the course refreshing the concepts of composition in OpenUSD.
We have our local layer stack
And then our arcs that compose content into the local layer stack

![](../../images/asset-modularity-instancing/slides/Slide24.gif)

The local layer stack functions as the point of refinement for all the content you've composed.  Robots can be articulated and assembly lines simulated.  Materials can be modified, variants can be selected.
Sparse overrides are often referred to as OpenUSD's superpower.  You can work modularly, assemble, and continue to refine downstream.

## Instancing

![](../../images/asset-modularity-instancing/slides/Slide25.jpg)

Encapsulating your assets in modular layers facilitates data reuse
Reuse amortizes the cost of a layer both within a scene and across scenes
Post composition, runtimes may be able to detect whether attribute values or parts are the same as a form of data duplication.
But data deduplication isn't free. You're trading time and algorithmic complexity for in-memory scene size
It would be nice to be able to say up front that a particular scene element is not open to refinement.
This is instancing. We can save scene graph processors lots of time by declarativity tagging parts of our scene as being not open to refinement on the local layer stack.

![](../../images/asset-modularity-instancing/slides/Slide26.jpg)

Modularity and Content Reuse Enables Centralized Editing: Change the prototype part—every instance updates throughout your facility or simulation.

Deduplication of Content: Reduces runtime resource usage (RAM, VRAM) than maintaining duplicate geometry/assets.
Instancing Accelerates Performance: Declarative deduplication.  Scenes with massive numbers of repeated items load and display faster.

Example: Instead of counting screws in every shelf in the digital warehouse, count them once on the prototype and multiply by the number of shelves

![](../../images/asset-modularity-instancing/slides/Slide27.jpg)

Key Terms:
* Prototype: A unique, shared sub-structure
* Instance: A repetition of a prototype within a scene
* Instanceable prim: The mutable root of an instance
