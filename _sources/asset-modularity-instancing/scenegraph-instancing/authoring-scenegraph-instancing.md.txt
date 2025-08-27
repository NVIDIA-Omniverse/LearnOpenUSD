# Authoring Scenegraph Instancing

Now, let’s talk about how to author instancing in OpenUSD, including:
* The meaning of instanceable metadata
* Explicit Instances & Implicit Prototypes
* Composition arcs and how they enable instancing

## Scenegraph Instancing

Setting instanceable = true tells OpenUSD to create one shared version (prototype) of an object that many instances can use as long as they share composition arcs.

Our warehouse has two references to "RobotArm" with instancing enabled.
This should generate one prototype subgraph.
Two instances of that prototype subgraph

``` usda
#usda 1.0

(
    defaultPrim = "Warehouse"
    metersPerUnit = 0.01
    upAxis = "Z"
)
def Xform "Warehouse"
{
    def "RobotArm_01" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
    }
    def "RobotArm_02" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
    }
    def "Converyor_01" (
        references = @./Conveyor.usd@
        instanceable = true
    )
    {
    }
    
}
```

Proxies and instance subgraphs are immutable, but the instanceable prim is mutable.

It has to be, if you couldn’t edit the instanceable prim, all of our crates would be on top of each other.

``` usda
#usda 1.0

(
    defaultPrim = "Warehouse"
    metersPerUnit = 0.01    
    upAxis = "Z"
)
def Xform "Warehouse"
{
    def "RobotArm_01" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {        double3 xformOp:translate = (10, 20, 0)
    }
    def "RobotArm_02" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
        double3 xformOp:translate = (10, 30, 0)
    }
    def "Conveyor_01" (
        references = @./Conveyor.usd@
        instanceable = true
    )
    {
        double3 xformOp:translate = (40, 20, 0)
    }
}

```

A common explainer mantra in learning OpenUSD is "explicit instances, implicit prototypes".

You tell OpenUSD the candidates for instancing, it figures out the prototypes implicitly from the authored composition arcs.

![](../../images/asset-modularity-instancing/slides/Slide31.jpg)

### Authoring Puzzle 

How many prototypes or instances get generated?

``` usda 

#usda 1.0

(
    defaultPrim = "World"
    metersPerUnit = 0.01    
    upAxis = "Z"
)
def Xform "Warehouse"
{
    def "Crate_01" (instanceable = True) {
       double3 xformOp:translate = (10, 20, 0)
    }

    def "Crate_02" (instanceable = True) {
       double3 xformOp:translate = (10, 30, 0)
    }

    def "Crate_03" (instanceable = True) {
       double3 xformOp:translate = (10, 40, 0)
    }
}

```

None, There’s no composition arcs on the instanceable prim so there’s nothing to generate prototypes from.

![](../../images/asset-modularity-instancing/slides/Slide33.jpg)

Instancing is an "opportunity" but not a "mandate" for optimization.  We’re going to introduce one more concept.

OpenUSD surfaces "proxies" as a read only scene graph element.  If you're writing a script, you can traverse the scene without considering instancing.
