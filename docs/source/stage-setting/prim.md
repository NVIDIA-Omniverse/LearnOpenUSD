# Prim

Primitives, or prims for short, are the building blocks of any OpenUSD scene, making understanding them essential for anyone working with 3D content creation and manipulation in the OpenUSD ecosystem.

<@ nvfunc kaltura 1_trdtyb7a @>

A prim is the core component within the USD framework. Think of a prim as a container that holds various types of data, attributes, and relationships which define an object or entity within a scene. A prim can be a type of imageable or non-imageable entity, such as a mesh, a material, or a light or an xform. Prims are organized in a hierarchical structure, creating a scenegraph that represents the relationships and transformations between objects in the scene.

Each prim has a unique identifier known as a path, which helps in locating it within the scene graph. For example, a prim’s path might be `/World/BuildingA/Geometry/building_geo`, indicating that it is a child of the `Geometry` prim, which itself is a child of the `BuildingA` prim, and so on.

### How Does It Work?

Prims can have various types of attributes associated with them, such as position, rotation, scale, material information, animation data, and more. These properties define the attributes and relationships of the objects they represent.

A key feature of USD prims is their ability to encapsulate data, allowing them to be shared, referenced, and instanced across different scenes and files. This promotes efficient data management, modularity, and collaborative workflows. Typical use cases include defining models, cameras, lights, or even groups of other prims. The ability to efficiently manage and manipulate these prims non-destructively is what makes USD so powerful in various industries where complex scenes are the norm.


### Working With Python

In Python, working with prims involves several methods using the USD Python
API:

```python
# Generic USD API command. Used to define a new prim on a stage at a specified path, and optionally the type of prim.
stage.DefinePrim(path, prim_type)

# Specific to UsdGeom schema. Used to define a new prim on a USD stage at a specified path of type Xform. 
UsdGeom.Xform.Define(stage, path)
	
# Retrieves the children of a prim. Useful for navigating through the scenegraph.
prim.GetChildren()
	
# Returns the type of the prim, helping identify what kind of data the prim contains.
prim.GetTypeName()

# Returns all properties of the prim.
prim.GetProperties()
```

### Key Takeaways

In this lesson, we covered what a prim is in the context of OpenUSD, its characteristics, and its role in building and managing 3D scenes. We also looked at how prims facilitate data encapsulation and sharing, which are critical for complex 3D project workflows. Understanding prims is foundational as we start working with OpenUSD.

Let's create our first prim in the next activity.
