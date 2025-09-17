# Introduction to Scenegraph Instancing

Now, let’s talk about how to author scenegraph instancing in OpenUSD, including:
* What is scenegraph instancing?
* The meaning of instanceable metadata
* Explicit Instances & Implicit Prototypes
* Composition arcs and how they enable scene graph instancing

## What Is Scenegraph Instancing?

Scenegraph--or native--instancing is the first implementation of instancing in OpenUSD that we will look at. Scenegraph instancing is a core feature of OpenUSD that turns prim hierarchies or subgraphs into prototypes that can then be shared by multiple copies within a scene. 

This approach is particularly valuable for large-scale scenes like digital twins, architectural visualizations, and any scenario where you need to represent many identical objects efficiently.

### Key Terms
![](../../images/asset-modularity-instancing/scenegraph-instancing-terms.png)

There are four key terms involved in scenegraph instancing that you need to be aware of:

* **Prototype**: A unique, shared sub-structure
* **Instance**: A repetition of a prototype within a scene
* **Instanceable Prim or Instance Prim**: The mutable root of an instance
* **Instance Proxy**: A read-only addressable stand-in of the prototype prims of an instance

Above we have a robot which has a gripper, an arm, and a base. We may have an instance of that prototype--a repetition of that prototype within a scene. The mutable root of the instance, "Robot_01," is called the instanceable prim. Lastly, the instance contains instance proxies so we can query "/Robot_01/Gripper" to learn more about what type of gripper the robot is using without having to map to the underlying prototype.

## How Does It Work?

To enable scenegraph instancing in USD, you need to set one value, the `instanceable` prim metadata. Setting `instanceable = true` tells OpenUSD to create one shared version (prototype) of an object that many instances can use as long as they share composition arcs.

Our warehouse has two references to "RobotArm" with instancing enabled.
To use the terminology we just introduced, this should generate one prototype and two instances of that prototype because the two robot arms are using the same reference.


```{code-block} usda
:emphasize-lines: 10-11,16-17,22-23
:linenos:

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

Setting `instanceable = true` is an explicit signal that OpenUSD should use instances and it basically says we're not going to put sparse overrides on the descendants of this prim. Proxies and instance subgraphs are immutable, but the instanceable prim is mutable.

It has to be, if you couldn’t edit the instanceable prim, we couldn't move our instances around and all of our robot arms would be on top of each other. 

```{code-block} usda
:emphasize-lines: 14,21,28
:linenos:

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
        double3 xformOp:translate = (10, 20, 0)
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

Note the unique `xformOp:translate` attributes values on each robot arm. Following this logic, it's natural to make it so instanceable prim allow you to have any arbitrary overrides you want, but just on the instanceable prim.

You may have noticed that the "Conveyor_01" prim also has `instanceable = true`. OpenUSD would create a prototype for this subgraph too, but based on this snippet, we could infer that there is only one instance using the prototype.

### Explicit Instances, Implicit Prototypes

A common explainer mantra in learning about scenegraph instancing is "explicit instances, implicit prototypes".

You tell OpenUSD the candidates for instancing, it figures out the prototypes implicitly from the authored composition arcs.

```{figure} ../../images/asset-modularity-instancing/explicit-instances-implicit-prototypes.mp4
Explicit instances, implicit prototypes
```

Here we start with our warehouse stage before instancing. If we set `instanceable = true` on objects in our scene, OpenUSD will figure out what the repetitions are based on the composition arcs to determine what the prototypes should be. The prototypes in this case corrolate with the four assets we created before hand: robot arm, rack, pallet, and box.

### Why Instance Proxies?

Scenegraph instancing should be thought of as an opportunity for optimization, but it's not a mandate. 

Instance proxies provide a convenient way for end users to see what an instance is made up of without having to follow the indirection from instance to prototype. 

Additionally, a script or a tool that reads OpenUSD data and is not performance sensitive can ignore instancing altogether. You can basically enable traversal of instance proxies and read the OpenUSD data as if instancing was not enabled. You don't get the performance benefits, but avoid some added complexity in your script.

## Examples

### Example 1: How Many Prototypes?

To drive home the points of how instancing works in OpenUSD here is a quick puzzle. How many prototypes and instances would be generated when you load the stage?

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

None. It's a bit of a trick question. Instancing is driven by your composition arcs. There are no composition arcs on the instanceable prims so there’s nothing to generate prototypes from.

OpenUSD basically says that's great that you want to instance these, but I'm not going to do anything here because there are no composition arcs for me to derive prototypes from.

That's why it's important to understand the difference between edits on a local layer stack versus edits through composition arcs.

## Key Takeaways

Scenegraph instancing in OpenUSD provides a powerful optimization technique for large-scale scenes by creating shared prototypes from repeated subgraphs. The `instanceable` metadata enables this functionality, allowing OpenUSD to automatically generate implicit prototypes from explicit instances based on composition arcs. Understanding the key terms—prototypes, instances, instanceable prims, and instance proxies—is essential for effectively implementing and managing scenegraph instancing in production workflows.