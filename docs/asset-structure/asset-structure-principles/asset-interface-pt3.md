# What Is an Asset Interface? (Part 3)
```usda
def Xform "Asset" {
    def Scope "Geometry" { ... }
    def Scope "Materials" { ... }
}

def Scope "World" {
    def Scope "environments" { ... }
    def Scope "actors" { ... }
}
```
To improve navigability, it's common to partition {term}`asset <Asset>` structures. Partitioning a hierarchy can prevent unintentional {term}`namespace <Namespace>` collisions between collaborators and avoid ambiguous semantics. For example, what does it mean for a Sphere to be parented to a Material?

Using scope {term}`prims <Prim>` is generally the best approach for these organizational primitives, as they don't have additional semantics like xform does with transform operations.

Similarly, it may be useful to group actors and environments under partitioning scopes. This not only aids navigability but also allows users to quickly deactivate all actors or environments by deactivating the root scope.

When organizing your prim hierarchy, also consider the following:

* **Naming Conventions**: A legible prim hierarchy should promote consistency for better readability.  
* **Access Semantics:** There are no restrictions on the fields that can be overridden on a prim, so it's important for collaborators to establish conventions for stable editing. This could include using single or double underscores to discourage users from authoring overrides or to indicate internal use.  
* **Embedded Context:** Embed context directly into assets to hint to users that these assets are intended to be included by {term}`reference <Reference>`.