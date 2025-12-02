# What Is Encapsulation?

{term}`Prims <Prim>` can be encapsulated or unencapsulated which has implications for {term}`referencing <Reference>` and other {term}`composition arcs <Composition Arcs>`. A prim is encapsulated when it is an ancestor of the referenced target prim. When a prim is encapsulated, it will be referenced along with its ancestor.

![](../../images/composition-arcs/image100.png)

Let’s take a look to see how it works. First, we’ll look at an example of a fully encapsulated reference. On the right side, we can see that we are making an external reference to `encapsulated.usd`.

![](../../images/composition-arcs/image77.png)

Here we can see that the contents of the reference include a cube that has a binding to a red material. When referencing `encapsulated.usd`, everything will be brought over that is contained under the xform `World`.

![](../../images/composition-arcs/image91.png)

Now let’s look at what we mean when we say unencapsulated.

On the right, we are making an external reference to `unencapsulated.usd`.

![](../../images/composition-arcs/image102.png)

Here are the contents of `unencapsulated.usd`.

Unlike our encapsulated example, the scope called “Looks” is not encapsulated inside of World.

So when we reference `unencapsulated.usd`, the cube will be brought over but the material binding will no longer work because the red material would not exist in the new context.