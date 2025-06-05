# Prim and Property Paths

In OpenUSD, a path is a type that represents the location of a prim within a scene hierarchy. Its string representation consists of a sequence of prim names separated by forward slashes (`/`), similar to file paths in a directory structure. The stage root, which serves as the starting point for the hierarchy, is represented by a forward slash (`/`).

For example, the path `/World/Geometry/Box` represents a prim named `Box` that is a child of a prim named `Geometry`, which is a child of the root prim named `World`.

### How Does It Work?

Paths in OpenUSD are handled through the `pxr.Sdf.Path` class to encode path data including prims, properties (both attributes and relationships), and variants.

Prims are indicated by a slash separator, which indicates the namespace Child (ex: `"/geo/box"`)

Period separators after an identifier is used to introduce a property (ex: `"/geo/box.weight"`)

Variants are indicated by curly brackets, like this: (ex. `"/geo/box{size=large}"`)

They are used to:

1. **Uniquely identify prims and properties**. Each prim and property in a scene has a unique path that distinguishes it from other prims and properties. 
2. **Navigate the scene hierarchy**. Paths allow you to traverse the scene hierarchy via the USD stage and access specific prims.
3. **Specify locations for authoring**. When creating or modifying prims, paths are used to specify where the prims should be placed in the hierarchy on the USD stage.
4. **Query and filter prims**. Paths can be used to filter and select specific prims based on their location in the hierarchy using `Sdf.PathExpression`.

### Working With Python

![Path Python](../../images/Path_Python.webm)

Here are a few Python functions relevant to paths in OpenUSD.

```python
# Import the Sdf class
from pxr import Sdf

# Return the path of a Usd.Prim as an Sdf.Path object
Usd.Prim.GetPath()

# Retrieve a Usd.Prim at the specified path from the Stage
Usd.Stage.GetPrimAtPath()
```


### Key Takeaways

Using `Sdf.Path` objects in OpenUSD provides a way to uniquely identify and locate objects (prims) within our scene hierarchy. We will use paths for authoring, querying, and navigating USD data effectively.



