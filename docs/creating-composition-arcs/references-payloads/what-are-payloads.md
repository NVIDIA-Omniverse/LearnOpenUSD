# Payloads

## What Are Payloads?

![](../../images/composition-arcs/image57.png)

{term}`Payloads <Payload>` are like {term}`references <Reference>`, but with the added ability of being able to {term}`load and unload <Load and Unload>` payloads on demand. Say you’re only interested in inspecting a single city block in a city scene. First, you’d load the {term}`stage <Stage>` of the whole city with all payloads unloaded. The stage would load quickly because we’ve deferred the loading of most of the {term}`assets <Asset>`. Then, you could navigate the scene hierarchy to find the city block or particular assets you are interested in and load just those payloads. When you load the payloads, the data from those {term}`layers <Layer>` and any other layers composed on the other side of the payload are composed into the scene.

By working this way, you can save yourself load time, memory, and interexercise since you are only loading and rendering a subset of the stage that you are interested in.

Payload {term}`composition arcs <Composition Arcs>` can be applied to the same {term}`prim <Prim>` in a list-editable way, just like references.

Payloads are weaker than references in the composition strength order (LIVRPS). On rare occasions, you may choose to use a payload instead of a reference to produce your desired composition order.