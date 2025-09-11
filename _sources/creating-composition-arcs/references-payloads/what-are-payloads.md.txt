# Payloads

## What Are Payloads?

![](../../images/composition-arcs/image57.png)

Payloads are like references, but with the added ability of being able to load and unload payloads on demand. Say you’re only interested in inspecting a single city block in a city scene. First, you’d load the stage of the whole city with all payloads unloaded. The stage would load quickly because we’ve deferred the loading of most of the assets. Then, you could navigate the scene hierarchy to find the city block or particular assets you are interested in and load just those payloads. When you load the payloads, the data from those layers and any other layers composed on the other side of the payload are composed into the scene.

## When and Why Do You Use Them?

By working this way, you can save yourself load time, memory, and interexercise since you are only loading and rendering a subset of the stage that you are interested in.

Payload composition arcs can be applied to the same prim in a list-editable way, just like references.

Payloads are weaker than references in the composition strength order (LIVRPS). On rare occasions, you may choose to use a payload instead of a reference to produce your desired composition order.