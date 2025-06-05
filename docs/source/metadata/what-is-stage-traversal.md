In the course [_Learning About Stages, Prims, and
Attributes_](https://learn.nvidia.com/courses/course-detail?course_id=course-v1:DLI+S-OV-17+V1), we touched on Stage Traversal. Let’s expand on that here.

---

**Stage traversal** is the process of traversing the scenegraph of a stage with the purpose of querying or editing the scene data. We can traverse the scenegraph by iterating through child prims, accessing parent prims, and traversing the hierarchy to find specific prims of interest.

Traversing stages works via the `Usd.PrimRange` class. Other methods like `stage.Traverse` use `Usd.PrimRange` as a base class.

Let’s review the Python functions we learned in the previous course that are relevant to traversal:

```python
# Open a USD file and create a Stage object
stage = Usd.Stage.Open('car.usda') 

# Traverses the stage of prims that are active
stage.Traverse() 

# Define a predicate to filter prims that are active and loaded
predicate = Usd.PrimIsActive & Usd.PrimIsLoaded

# Traverse starting from the given prim and based on the predicate for filtering the traversal
Usd.PrimRange(prim, predicate=predicate)
```

This module focuses on improving efficiency by limiting the number of prims that the process visits while traversing the stage.

### How Does It Work?

As a first step toward optimizing the traversal process, we can filter it based on the type of the prim, such as Scope or Xform. This enables us to be more efficient and targeted when we take the next step of traversing through the children of a prim.

`Usd.PrimRange` is another traversal method that, unlike `Traverse()`, can traverse through a pseudo root prim.

### Working With Python

For filtering prims during traversal, some Python functions are particularly useful:

```python
# Check whether the prim is of type Scope
if UsdGeom.Scope(prim) 

# Get a specific child prim named "Environment" under the default prim
default_prim.GetChild("Environment")`
```

### Key Takeaways

Traversal is how we navigate the scenegraph and query scene data. Traversal can be made more efficient by limiting the number of prims it visits.

Let's try out some traversal functions in the next activity.



