# Encapsulation and Refinement

Both {term}`inherit <Inherit>` and {term}`specialize <Specialize>` arcs can target an encapsulated or unencapsulated {term}`prim <Prim>` as their source prim. Depending on whether the source prim is encapsulated or not, the broadcasting behavior of the inherits/specializes arc changes when the destination prim is referenced into another {term}`layer stack <Layer Stack>`.

Inherits/specializes arcs become more useful when instancing comes into play. That will be covered more in‑depth in a future module.