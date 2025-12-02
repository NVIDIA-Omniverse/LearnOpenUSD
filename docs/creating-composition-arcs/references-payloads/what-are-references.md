# References

## What Are References? 

Let’s say we want three identical {term}`prims <Prim>` in a scene.

![](../../images/composition-arcs/image67.png)

Sublayering a {term}`layer <Layer>` multiple times won't work in this case. In the above image, the same sphere would just be redefined three times because there is no way to specify that the copies of the sphere should be defined at different {term}`paths <Path>` in the prim hierarchy (e.g. siblings of each other) 

![](../../images/composition-arcs/image78.png)

Instead, you may want to {term}`reference <Reference>` a layer onto multiple prims to make multiple copies of the same content. References graft a prim hierarchy from one layer onto a prim of another layer, making them ideal for modularity and reusability.

The referenced prim undergoes a prim name change and {term}`path translations <Path Translation>` to reflect the new {term}`namespace <Namespace>` of the prim that the referenced prim hierarchy is being grafted onto.

In this example, the Prim.usda content is referenced 3 times under 3 differently named prims.

## When and Why Do You Use Them?

The primary use for references is to compose smaller units ({term}`assets <Asset>`) of scene description into larger aggregates. Libraries of assets can be developed in parallel by multiple contributors and modularly aggregated to build up a large scene. The same assets can also be reused to build out different scenes or scenarios while reducing duplication of effort.

One example would be a digital twin of a large factory environment that can consist of various assets from disparate sources like: boxes, machinery, conveyor belts, shelving, etc. Each asset can be referenced one or more times to build out an entire factory.

![](../../images/composition-arcs/image84.png)

References can be external, targeting a prim from a different layer, or they can be internal, targeting a prim within the same USD layer. Let’s take a look at what that looks like in the example above.

In the USDA file to the right, we have defined a couple of prims. The `red_cube_01` and `red_cube_02` are referencing from another layer. Below that we have defined `blue_cube_01`, and `blue_cube_02` and `blue_cube_03` are referencing `blue_cube_01` that we have defined internally in the current layer.

Usually, references are external, but it can be very convenient to use this internal referencing scheme to achieve specific goals, such as {term}`instancing <Instancing>`.