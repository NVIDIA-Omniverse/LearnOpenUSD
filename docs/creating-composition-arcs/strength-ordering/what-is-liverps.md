# What Is LIVERPS?

```{include} ../../_includes/LIVRPSvLIVERPS.md
```

![](../../images/foundations/strength_ordering.png)

Throughout this module, we’ve been talking about individual {term}`composition arcs <Composition Arcs>` and talking about how some are stronger or weaker than others. These arcs adhere to a set of {term}`strength ordering <LIVERPS Strength Ordering>` rules that we affectionately refer to as LIVRPS (pronounced “liver peas”), an acronym that captures the individual arcs according to their strength, with **local** opinions being the strongest and **{term}`specialize <Specialize>`** arcs being the weakest.

The LIVRPS acronym captures all of the operations to compose data from {term}`layers <Layer>` onto the {term}`stage <Stage>`, in the order in which each operation is applied.

Why do we need strength ordering rules? In OpenUSD, multiple {term}`layer stacks <Layer Stack>` and their opinions are composed together to create the composed {term}`stage <Stage>`. We need strength ordering to determine which {term}`opinion <Opinions>` gets composed in the final stage.

![](../../images/composition-arcs/image14.png)

**What is Layer Stack?**

A layer stack is the ordered set of layers resulting from the recursive gathering of all {term}`sublayers <Sublayer>` of a layer, plus the layer itself as first and strongest. This also includes all local composition arcs like internal {term}`references <Reference>`, internal {term}`payloads <Payload>`, {term}`variant sets <Variant Set>`, {term}`inherits <Inherit>`, and specializes. Multiple layer stacks are composed together using references and payloads.

![](../../images/composition-arcs/image80.png)

A local opinion is authored directly, without any other {term}`composition <Composition>` operations, in a layer or any of its recursive sublayers.

In the USDA file on the right, we have a local opinion which is our radius on our sphere.

![](../../images/composition-arcs/image85.png)

In this stage with one layer, there is only one {term}`prim spec <Prim Spec>` and {term}`property spec <Property Spec>` for the Sphere prim, so the composition is obvious. The composition is just the radius of the sphere, 2.0.

![](../../images/composition-arcs/image42.png)

In the case where a layer has a sublayer, opinions authored directly in both layers are considered "local".

Since we have an {term}`override <Over>` on the sphere where the radius is 2.0, this is our local opinion on the root layer. This is stronger than the sublayer's local opinion setting the radius to 1.0.

For any given layer stack, the opinion of the root layer is considered the strongest, followed by any opinions that appear in the ordered list of sublayers.

![](../../images/composition-arcs/image70.png)

The local (L) component of LIVRPS also consists of all sublayers of sublayers as they all belong to the same layer stack. When opinion strength is evaluated, the strength-ordered list of sublayers is populated by recursively gathering sublayer opinions in a depth-first order.

![](../../images/composition-arcs/image13.png)

In this case, `sublayer1.usda` is higher in the list than `sublayer2.usda`. Therefore, the opinions in `sublayer1A.usda` and `sublayer1B.usda` are stronger than opinions in `sublayer2.usda`, because they are sublayers of `sublayer1.usda`.


![](../../images/composition-arcs/image35.png)

Now let’s think about this as a layer stack. A layer stack consists of a layer and all of its recursive sublayers. Any direct opinion authored in any layer in the stack is considered local to that layer stack.

It’s important to note that composition operations, such as references and payloads, are considered in the context of a layer stack, not an individual layer.

![](../../images/composition-arcs/image12.png)

LIVRPS answers the questions--given a {term}`prim <Prim>` on a USD stage, how do I build the {term}`prim stack <Prim Stack>` that represents it? How do you build {term}`property stacks <Property Stack>` for the {term}`properties <Property>` on the prim?

![](../../images/composition-arcs/image16.png)

The order of the layer stack changes the composition of the scene.

![](../../images/composition-arcs/image50.png)

The LIVRPS acronym represents not only the different composition operations, but the order in which they are applied. This means that, when composing the opinions within a layer stack:

- Local opinions are ordered first (strongest)
- Opinions from inherit arcs are ordered next
- Opinions from variant set arcs are ordered next
- Opinions from reference arcs are ordered next
- Opinions from payload arcs are ordered next
- Opinions from specialize arcs are ordered last (weakest)

LIVRPS applies recursively within each composition context (layer stack)