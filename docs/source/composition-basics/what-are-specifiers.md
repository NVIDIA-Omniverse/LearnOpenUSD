Specifiers in OpenUSD convey the intent for how a prim or a primSpec should be interpreted in the composed scene. The specifier will be one of three things: `Def`, `Over` or `Class`.

### How Does It Work?

![Specifier Def](../../images/Specifiers_Def.webm)

`Def`, which is short for _define_ , defines the prim in the current layer. `Def` indicates a prim exists, is present on the stage and available for processing.

The resolved specifier of a prim--essentially, which specifier wins when the composition is completed--determines which traversals (like rendering) will visit that prim. Default traversals will only visit defined (`def`), non-abstract prims. Abstract prims are those that resolve to the `class` specifiers. `Over`, the weakest specifier, will resolve to either a `def` or
`class` specifier.

![Specifier Over](../../images/Specifiers_Over.webm)

`Over`, which is short for _override_ , holds overrides for opinions that already exist in the composed scene on another layer. The `over` will not translate back to the original prim, and is what enables non-destructive editing workflows, such as changing a property of a prim, like its color, in another layer.  

![Specifier Class](../../images/Specifiers_Class.webm)

`Class` prims are essentially a blueprint. They abstract and contain opinions that are meant to be composed onto other prims (more on this when we cover Composition). It’s worth noting that `class` prims are intended as the target of a reference, payload, inherit, or specialize composition arc--a concept we’ll review in a future module.

Prims that resolve to `class` specifiers will also be present and composed on a stage, but won’t be visited by default traversals, meaning it will be ignored by traversals such as the rendering API, Hydra.

### Working With Python

![Specifier Python](../../images/Specifiers_Python.webm)

Below is an example of how we can get or set a prim's specifier using Python.

```python
# Get a prim’s specifier
prim.GetSpecifier()

# Set a prim’s specifier
prim.SetSpecifier(specifier)
```

It's helpful to look at USDA files to understand how USD encodes specifiers in a USD layer. In this example, we're defining a new prim called `"Box"` with the type `Cube` and a `size` property set to `4`. The `def` specifier indicates that box is being concretely defined on the stage. 
```usda
def Cube “Box” {
    double size = 4
}
```

The `over` specifier sparsely modifies the `size` property without defining anything else about the prim; in this case, `size` is overriden to have a value of `10`. With an override like this, we may be trusting that the box has been defined in another layer, for example.

```usda
over “Box” {
    double size = 10
}
```
Lastly, we're authoring a new prim as a `class` called `"_box"`. This can be used as  a reusable template in the USD scene.
```
class “_box” {
    double size = 4
}
```
### Key Takeaways

Again, every prim will have a specifier. To have a prim present on the stage and available for processing you would define (`def`) that prim. You can use override specifiers, (`over`), to hold opinions that will be applied to prims in another layer and leverage non-destructive editing workflows, while class specifiers (`class`) can be leveraged to set up a set of opinions and properties to be composed by other prims.



