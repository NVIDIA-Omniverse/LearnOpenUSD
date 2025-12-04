# Specializes

## What Are Specialize Arcs?

![](../../images/composition-arcs/image25.png)

The {term}`specialize arc <Specialize>` is similar to the {term}`inherit arc <Inherit>`, but provides the ability to broadcast specs ({term}`prim specs <Prim Spec>` or {term}`property specs <Property Spec>`) across {term}`layer stacks <Layer Stack>` as fallback values. The spec from the specializes source {term}`prim <Prim>` is applied to all specializes destination prims if there isn’t another authored opinion for that spec.

## When and Why Do You Use Them?

Specializes can be used like more traditional OOP (object-oriented programming) inheritance. Any spec authored as specializes can serve as a default and fallback. In OOP, objects that override their class members will ignore updates made to those class members. Conversely, objects that are still using the value defined by the class will fallback and reflect any runtime changes made to the class members.

In the *Exercise: Experimenting with Specializes* unit we will utilize a hands-on demonstration to better illustrate how the specialize arcs work.

