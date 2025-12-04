# Sublayers

![](../../images/composition-arcs/image59.png)

## What Are Sublayers?

{term}`Sublayers <Sublayer>` are a list of USD {term}`layers <Layer>` that are ordered by opinion strength (i.e. the first layer is stronger than the last layer). Each layer overlays on top of each other and provides opinions (specs). When a layer is composed as a sublayer, all of its contents are added to the destination layer in an “include” fashion without any remapping.

## When and Why Do You Use Them?

When working with large scenes, being able to have each workstream work in their own smaller, manageable sublayers makes it easier to work in the scene. For example, one workstream could be working on lighting while another workstream works on {term}`asset <Asset>` layout. These sublayers are independent but can be composed together. That way, as new assets are added in one workstream, the lighting workstream does not have to change. Each workstream can also work independently without blocking each other.

![](../../images/composition-arcs/image64.png)

Starting from left to right, we have our root layer that contains two sublayers: `sublayerB` and `sublayerA`. Our root layer also contains an Xform called `World` with a scope called `Geometry`.

In `sublayerA`, we also have `World` and `Geometry`. Under `Geometry`, we have defined a `Cube` of size `100`. In `sublayerB`, the setup is similar to `sublayerA`, except under `Geometry` we defined a `Sphere` of radius `50`.  On the far right, we see the composed result. This composed result shows both a sphere and a cube. 

![](../../images/composition-arcs/image103.png)

Now let’s add a differing opinion for the size of the `Cube` in `sublayerB`, shown in green in the image.

If we look back at our root layer on the far left, we see that `sublayerB` comes before `sublayerA`, meaning the authored opinions in `sublayerB` will outweigh `sublayerA`’s opinions. This is why in the composed result `sublayerB`’s opinion for the cube’s size of `50` was used instead of size `100` from `sublayerA`.