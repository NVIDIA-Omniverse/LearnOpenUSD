# Inherits

## What Are Inherit Arcs?

![](../../images/composition-arcs/image7.png)

The inherit arc shares some commonalities with inheritance in programming. In the example above, we're establishing an inherits arc so that `/World` prim inherits from `/_cube_asset`. Any prims or properties defined or overridden within the `/_cube_asset` hierarchy are applied to World. This sounds a lot like a reference, but the key difference is that inherit arcs allow modifications to the source prim to be broadcast to all inheriting prims across different layer stacks, while references create isolated instances.

## When and Why Do You Use Them?

When you are defining reusable assets, it's useful to include an inherit arc with an unencapsulated source prim so that you can apply overrides to all references of an asset within another layer stack.

![](../../images/composition-arcs/image32.png)

After establishing the inherit arc, we can modify the source prim and any of its descendants in any stronger layer including across references (layer stacks) and it is broadcast and applied to all prims that inherit it.

The source prim becomes a global namespace that can be edited at any stronger layer in the composition.

We can always tweak individual copies of the prim in `Scenario_A` after the broadcast by just authoring another opinion in a stronger layer.

![](../../images/composition-arcs/image10.png)

The broadcast only applies to the context in which it is authored. The opinion authored in `Scenario_A` doesn't affect `Scenario_B`. This is different from authoring a change to the `cube_asset` directly that would affect all stages that reference it. (i.e. `Scenario_A` and `Scenario_B`)

![](../../images/composition-arcs/image3.png)

We use the “class” specifier in USD when authoring a prim hierarchy that is meant to be inherited. This serves two purposes:

* It communicates to developers or end users that this is a prim that is meant to be used as a part of inherits or specializes arcs.
* Hydra does not image (or render) a prim with a “class” specifier or any of its descendants. This is the type of behavior you typically want for purely abstract data that is meant to be leveraged by another prim.

