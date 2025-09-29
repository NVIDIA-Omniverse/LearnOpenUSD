# Variant Sets

## What Are Variant Sets?

![](../../images/composition-arcs/image9.png)

![](../../images/composition-arcs/image43.png)

Variant sets allow you to define variations or alternative representations of the same dataset that can be switched at runtime. The most common use case for this is to be able to define a singular asset, while enabling multiple representations of that asset.

For example, a character that has multiple outfits could be authored with a variant set that controls which outfit should be used for a given shot or scenario. This greatly reduces the complexity of managing such a character. Without a mechanism like variant sets, you would need to track the character and the clothing separately, and assemble them on-demand whenever a particular character and outfit combination is needed.

A variant set serves as a controller of variations. We call the variations “variants” in OpenUSD. Only opinions of the selected variant are composed on the stage. All other variants are effectively not traversed or included.

It’s up to the author to decide what “type” of variations a variant set controls. There are no rules for what a variant set can add or modify, but it is helpful to limit the scope of a variant set so that the results are more predictable when users are blindly selecting a variant.

A variant set is added to a prim and its variants can manipulate the prim and any of its descendants. Let’s go through a few things a variant can do within its hierarchy.

---

### Variants can sparsely override properties on the prim or any descendant prim.

![](../../images/composition-arcs/image38.png)

In this example we can see that there are two variants that override the diffuse color of the cube material; one variant is overriding the color to be blue, and the other to green.

---

### Variants can define new descendant prims.

![](../../images/composition-arcs/image82.png)

Here we have two variants, where one variant defines one cube and the other defines two cubes.

---

### Variants can be used to author new composition arcs that would only exist within that variant.

![](../../images/composition-arcs/image96.png)

We can author new composition arcs that would only exist in the variant. For example, one variant can reference a blue material from a materials layer, and another variant can reference a green material from the same layer.

## When and Why Do You Use Them?

![](../../images/composition-arcs/image23.png)

You could author a single variant set on an asset to control a single set of options, like different materials on a cube in the image above.

![](../../images/composition-arcs/image40.png)

Or, you could create multiple variant sets for different purposes that can be controlled separately to produce many different combinations.

A common pattern is to author geometric and shading variant sets. Geometric variant sets control changes in an asset’s geometry and shading variants control changes in an asset’s materials.

Let’s consider another example. If you wanted to have a character with two geometry options where the character is wearing a “hat” or “no hat” and two material options of “dry” and “wet”, you could produce four different combinations.

Keep in mind that combinations are not “free”. You have to author relevant data for each combination and it is easy to run into two risks:

- It’s easy to get carried away with adding too many variant sets and creating variant combinations that will never be used, like a wet character without a hat.
- You may choose to not author data for all combinations, but that can create bad UX when end-users try to use a non-functional combination.
