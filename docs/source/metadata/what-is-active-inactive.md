![](../../images/ActiveInactive_Definition.webm)

In OpenUSD, all prims are active by default. Making a prim inactive models a non-destructive deletion of a prim from a stage. Deactivating a prim provides a way to temporarily remove, or prune, prims and their descendants from being composed and processed on the stage, which can make traversals more efficient.

An active prim and its active child prims will be visited and processed during stage traversals and operations. However, by making a prim inactive by setting its "active" metadata to _false_, we prevent that prim itself from being visited. This also prevents its descendant prims from being composed onto the
stage.

```python
# Make the prim at /Parent inactive
stage.GetPrimAtPath('/Parent').SetActive(False)
```

Deactivating a prim is a non-destructive operation–-the prim still exists in the scene description, but it is pruned from the composed stage view until reactivated. This is effectively the way to delete a prim from the stage.

### How Does It Work?

Deactivation is useful for managing scene complexity and scalability by pruning unnecessary scene data. It provides a way to non-destructively remove parts of the scene graph without permanently deleting them.

When a prim is deactivated, it has the following effects:

* The prim itself will be excluded from default stage traversals as determined by the `UsdPrimDefaultPredicate`.
* All scene description for the deactivated prim's descendants will not be composed onto the stage.

However, the inactive state can be overridden by stronger layer opinions that set the "active" metadata to _true_ for that prim. This allows selective reactivation of pruned subtrees.

![ActiveInactivePython](../../images/ActiveInactive_Python.webm)

### Working With Python

We can use the following Python functions to set the "active" metadata on a prim and check to see if the prim is currently active on the stage.

* `UsdPrim.SetActive(bool)` - Set the "active" metadata for a prim
* `UsdPrim.IsActive()` - Return whether a prim is currently active on the stage

### Key Takeaways

![](../../images/ActiveInactive_Inactive.webm)

The active/inactive behavior in OpenUSD allows for non-destructive pruning of scene data from the composed stage view. Deactivating prims helps manage scene complexity by temporarily removing unnecessary scene elements, while still
preserving the ability to reactivate them later. This pruning mechanism is an important tool for optimizing performance and managing large, complex USD scenes in production pipelines.



