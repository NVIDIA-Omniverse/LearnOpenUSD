Welcome to this lesson on OpenUSD stages, a core element in 3D scene description. Understanding OpenUSD stages enables collaboration across various applications and datasets by allowing us to aggregate our data in one place.

At its core, an OpenUSD stage presents the scenegraph, which dictates what is in our scene. It is the hierarchy of objects, called prims. These prims can be anything from geometry, to materials, to lights and other organizational elements. This scene is commonly stored in a data structure of connected nodes, which is why we refer to it as the scenegraph.

<@ nvfunc kaltura 1_cm4ehcvo @>

### How Does It Work?

Think of it as a scene, a shot or a scenario we may open up in a DCC. A stage could be made up entirely with just one USD file (like a robot), or it could be a USD file that includes many more USD files (like a factory with many robots). The stage is the composed result of the file or files that may contribute to a scenegraph.

Composition is the result of the algorithm for how all of the USD files (or layers, in USD parlance, as USD content need not be file-backed) should be assembled and combined. We’ll look at composition more closely later on.

![A stage with USD assets in the scenegraph.](../../images/11.png)

In the example above, we have a stage, which contains USD assets in the scenegraph, like `Car.usd`, `Environment.usd`, `Lighting.usd` and `Cameras.usd`. This organization is useful for aggregating data for architectural workflows, factory planning and manufacturing, visual effects in filmmaking--anywhere where multiple assets need to be combined and integrated
seamlessly.

Each one of these USD assets can also be opened independently of the current stage. In this case, if we opened `Car.usd`, it would have its own stage that would be composed of `Simulation.usd` and `Geometry.usd`.

When we leverage OpenUSD stages properly, we can enable:

* **Modularity** : Stages enable the modification of individual elements without altering the original files (“non-destructive” editing), fostering a flexible workflow upon modular scene elements.
* **Scalability** : Stages can manage large datasets efficiently (e.g., via payloads, which we’ll learn more about when we dive deeper into composition).

### Working With Python

Creating a USD stage is the first step to generating a new USD scenegraph. In Python, we can use the functions:

```python
# Create a new, empty USD stage where 3D scenes are assembled
Usd.Stage.CreateNew()
  
# Open an existing USD file as a stage
Usd.Stage.Open()
  
# Saves all layers in a USD stage
Usd.Stage.Save()
```

### Key Takeaways

An OpenUSD stage is the key to managing and interacting with 3D scenes using USD. The stage enables non-destructive editing, layering, and referencing, making it ideal for complex projects involving multiple collaborators. Leveraging OpenUSD stages properly can significantly enhance the efficiency
and quality of 3D content production.

In the next lesson, we'll be talking about the rendering architecture within OpenUSD that lets us visualize our stages.



