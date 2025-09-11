# Specifiers

## What Are Specifiers?

Specifiers in OpenUSD convey the intent for how a prim or a primSpec should be interpreted in the composed scene. The specifier can be one of three values: `def`, `over` or `class`.

### How Does It Work?

![Specifier Def](../images/foundations/Specifiers_Def.webm)

`def`, which is short for _define_ , defines the prim in the current layer. `def` indicates a prim exists and concretely defined on the stage.

The resolved specifier of a prim--essentially, which specifier wins when the composition is completed--determines which stage traversals (like rendering) will visit that prim. Default traversals will only visit defined (`def`), non-abstract prims. Abstract prims are those that resolve to the `class` specifiers. `over`, the weakest specifier, will resolve to either a `def` or `class` specifier.

![Specifier Over](../images/foundations/Specifiers_Over.webm)

`over`, which is short for _override_ , holds overrides for opinions that already exist in the composed scene on another layer. The `over` will not translate back to the original prim, and is what enables non-destructive editing workflows, such as changing a property of a prim, like its color, in another layer.  

![Specifier Class](../images/foundations/Specifiers_Class.webm)

A `class` prim essentially signals that it is a blueprint. `class` prims abstract and contain opinions that are meant to be composed onto other prims. It’s worth noting that `class` prims are intended as the target of a reference, payload, inherit, or specialize composition arc or as a relationship target for a PointInstancer. These are concepts we'll cover in a later lesson.

Prims that resolve to `class` specifiers will also be present and composed on a stage, but won’t be visited by default stage traversals, meaning it will be ignored by traversals such as those used for rendering.

### Working With Python

![Specifier Python](../images/foundations/Specifiers_Python.webm)

Below is an example of how we can get or set a prim's specifier using Python.

```python
# Get a prim’s specifier
prim.GetSpecifier()

# Set a prim’s specifier
prim.SetSpecifier(specifier)
```

It's helpful to look at USDA files to understand how USD encodes specifiers in a USD layer. In this example, we're defining a new prim called "Box" with the type Cube and a `size` property set to `4`. The `def` specifier indicates that box is being concretely defined on the stage. 
```usda
def Cube "Box" {
    double size = 4
}
```

The `over` specifier sparsely modifies the `size` property without defining anything else about the prim; in this case, `size` is overriden to have a value of `10`. With an override like this, we may be trusting that the box has been defined in another layer, for example.

```usda
over "Box" {
    double size = 10
}
```
Lastly, we're authoring a new prim as a `class` called `"_box"`. This can be used as a reusable template in the USD scene.
```usda
class "_box" {
    double size = 4
}
```

## Key Takeaways

Again, every prim will have a specifier. To have a prim present on the stage and available for processing you would define (`def`) that prim. You can use override specifiers, (`over`), to hold opinions that will be applied to prims defined in another layer and leverage non-destructive editing workflows, while class specifiers (`class`) can be leveraged to set up a set of opinions and properties to be composed by other prims.



