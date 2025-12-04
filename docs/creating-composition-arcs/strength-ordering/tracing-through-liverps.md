# Tracing Through LIVERPS
Let's take a look at LIVRPS in action through a series of examples. The following examples will present different {term}`composition <Composition>` scenarios and trace through LIVRPS step-by-step to better understand the composition algorithm.

## Composition of a Single Layer

```{kaltura} 1_vtrfpupl
```

## Composition Involving Sublayers

```{kaltura} 1_c5goy7bm
```

One interesting thing to note from this example is that even though `workstreamA.usd` has a weaker {term}`sublayer <Sublayer>` strength than `workstreamB.usd` because it comes later in the order, `workstreamA.usd` still contains the winning opinion because it has a Local opinion where the root layer and other sublayer do not.

## Composition Involving Two Layer Stacks via References

```{kaltura} 1_syc3urwy
```

## Composition Involving More Nested Layer Stacks

```{kaltura} 1_ea08m71w
```

These examples are all studies of the composition algorithm for just one {term}`property <Property>`. You can imagine how complex debugging composition can be when this is scaled out to thousands of {term}`prims <Prim>` with tens of properties each and different combinations of {term}`composition arcs <Composition Arcs>` operating on subsets of these prims and properties.