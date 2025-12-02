# Introduction to Point Instancing

## What Is Point Instancing?

Point instancing is implemented as a {term}`schema <Schema>` in OpenUSD--the PointInstancer {term}`prim <Prim>` type.

PointInstancer uses array {term}`attributes <Attribute>` to describe points in 3D space. Additionally, explicit prototypes represented by {term}`prim hierarchies <Namespace>` in the {term}`stage <Stage>` are specified as {term}`relationship <Relationship>` targets on the PointInstancer. By combining the points, prototypes, and an index array to map the points to prototypes, OpenUSD is able to handle hundreds of thousands of repetitions very compactly in this vectorized format.

```{seealso}
See the {usdcpp}`UsdGeomPointInstancer Details` documentation to learn more about PoinstInstancers.
```

Compared to [scenegraph instancing](../authoring-scenegraph-instancing/scenegraph-instancing-intro.md), PointInstancers can be less user-friendly and trickier to refine because most of scene description is hidden away in large arrays that are not as human-readable. 

Point instancing is designed for massive numbers of simpler items where the overhead of an instance outweights the benefits of reuse. What does this mean? Think about leaves on a tree. You might have a 100,000 leaves on a tree. If you started down the path of using scenegraph instancing for this, you would need to define each leaf repetition and you would end up with 100,000 {term}`instanceable <Instanceable>` prims: "Leaf_000001", "Leaf_000002", "Leaf_000003", etc. Do you really need this in your scenegraph? Is this useful data for anyone?

That's where point instancing is a clear winner.

## How Does It Work?

We will talk through a concrete example of point instancing packing peanuts within a box. A single box may not have a lot of packing peanuts, but they are not prims we want to enumerate in our scenegraph.

![](../../images/asset-modularity-instancing/packing-peanuts-pointinstancer.png)

```usda

#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 0.01    
    upAxis = "Z"
)
def PointInstancer "PackingPeanuts"
{
    rel prototypes = [<Prototypes/Peanut_01>,
                      <Prototypes/Peanut_02>]
    int[] protoIndices = [0, 0, 0, 1, ...]
    
    point3f[] positions = [...]
    quath[] orientations = [...]
    float3[] scales = [...]

    over Scope "Prototypes" {
        def "Peanut_01" (
            references = @./Peanut.usd@
            variants = {string color = "blue"}
        )
        {
        }
        def "Peanut_02" (
            references = @./Peanut.usd@
            variants = {string color = "red"}
        )
        {
        }
    }
}
```

Point instancing is a schema-based instancing solution, so we need to start by defining a PointInstancer prim. The PointInstancer includes the following mandatory properties:
1. `prototypes`: A relationship targeting the prim hierarchies that the PointInstancer should use as instance prototypes.
2. `protoIndices` Declares an instance of a prototype. Each element in the array maps a point to a prototype id.
3. `positions` The points in local space where each instance is located.

`orientations` and `scales` are optional, but can be used to fully pose each instance. `ids` is an optional attribute if you want explicit control over the integer id of each instance. Otherwise, each instance id is inferred from the element index in the `protoIndices` array. (e.g. index `0` in protoIndices is instance id `0`).

As a best practice, we defined the prototypes under a Scope as a descendant of the PointInstancer. Unlike implicit prototypes in scenegraph instancing, you need to explicitly define each of the prototypes for your PointInstancer. We purposefully use an {term}`over <Over>` {term}`specifier <Specifier>` for the Scope to keep the prototypes from being traversed by default traversals. This is a way that we can signal that these prototypes don't need to be rendered and should be skipped. The instances are typically what we want rendered.

Let's spend a little bit of time breaking down how points are mapped to prototypes. In the example, `protoIndices` shows `[0, 0, 0, 1, ...]`. The integers repesent an indices in the `prototypes` array. `0` maps to `<Prototypes/Peanut_01>` and `1` maps to `<Prototypes/Peanut_02>`. This means that the the first three points are using `<Prototypes/Peanut_01>` and the following point is using `<Prototypes/Peanut_02>`.

## Querying and Overriding Point Instances

![](../../images/asset-modularity-instancing/packing-peanuts-array.png)

Many of the PointInstancer properties are array attributes. There's no easy way to ask us for information about individual instances here. Much of the data has been vectorized. You potentially have giant arrays of positions, orientations, scales, etc. You have to index into those arrays yourself to query data about a particular instance or to override any of them.

Additionally, at the moment, there is no way to do sparse overrides on arrays. If you want to move even just a single point in a PointInstancer, you need to author the entire `positions` array again for the new {term}`opinion <Opinions>`.

```{code-block} usda
:caption: A PointInstancer override requiring full arrays for each timesample.

#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 0.01    
    upAxis = "Z"
)
over "PackingPeanuts"
{
    point3f[] positions.timeSamples = {
       1: [...],
       2: [...],
       ...
       100: [...]
    }
    quath[] orientations.timeSamples = {
       1: [...],
       2: [...],
       ...
       100: [...]   
    }
}
```

Keep this in mind as you perform downstream overrides and considerations you may need to make about things like USD {term}`layers <Layer>` format (i.e. USDA vs {term}`USDC <Crate File Format>`).