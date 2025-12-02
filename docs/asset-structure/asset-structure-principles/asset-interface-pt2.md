# What Is an Asset Interface? (Part 2)
Now that we’ve had a chance to experiment with creating an {term}`asset <Asset>` with an entry point {term}`prim <Prim>`, let’s get back to our lesson on asset interfaces. 

![](../../images/asset-structure/image66.png)

Library assets (like a palette of related materials) may not have a single entry point. Each defined material may be individually referenced by  downstream assets.  

![](../../images/asset-structure/image37.png) 

For library assets with a large number of entry points, **scope** prims can be used to group and organize the entry points.

```usda
#usda 1.0

def Scope "World" {
  def "City" (references = @uri:/project/city.usd@) {}
  def "TaxiCab" (references = @uri:/project/taxi_cab.usd@) {}
}
```
Sometimes, an entry point is simply a convention for a particular type of asset. For example, the `World` prim doesn’t have a special role; it’s just the agreed-upon parent that keeps the scene outside of the root {term}`namespace <Namespace>`.

Even if it's not set as a default prim, we don’t need to overthink what the entry point is. 

## Encapsulation

![](../../images/asset-structure/image12.png)

Content authors should practice encapsulation with their prim entry points. Encapsulation means ensuring that everything intended to be part of an asset, rooted at a specific entry point, is a descendant of that prim entry point. This includes any {term}`relationship <Relationship>` targets.