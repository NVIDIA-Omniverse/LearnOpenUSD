# Model Hierarchy Considerations

When creating a {term}`model hierarchy <Model Hierarchy>`, there are four essential factors to keep in mind. These hierarchies should be operational, shallow, consistent, and extensible. Let's explore each of these aspects in more detail.   
![](../../images/asset-structure/image61.png)

## Operational

![](../../images/asset-structure/image62.png)

{term}`Component <Component>` and {term}`assembly <Assembly>` {term}`models <Model>` should be easily referenced in other contexts, and they should include all essential dependencies, such as material bindings or skeleton setups, that downstream users require. 

It’s important to note that the definition of an operational model may vary by site and pipeline. For example, some pipelines might support geometry-only component models, which are designed to be shaded in downstream assembly models.

## Shallowness

{term}`Asset <Asset>` structures should encourage a shallow model hierarchy. The {term}`kind <Kind>` {term}`metadata <Metadata>` is explicitly read during {term}`composition <Composition>` for all members of the model hierarchy, with costs minimized in a shallow structure. A deep model hierarchy introduces a small but measurable overhead to composition and misses out on performance gains from pruned traversals. A {term}`gprim <Gprim>` tagged as a component is a sign that a model hierarchy is “deep”.

## Consistency

As the language and expectations around components, {term}`subcomponents <Subcomponent>`, and assemblies evolve within an ecosystem, it’s crucial that an asset consistently represents one of these concepts. For instance, it’s common to expect component models to be fully packaged and renderable, with their geometry and materials completely specified and organized into Geometry and Materials scopes. 

However, the practice of referencing component models within other component models and reclassifying them as subcomponent prims can make asset navigation more complex, as material {term}`prims <Prim>` can become nested under the Geometry scope. 

If this complexity is a concern, consider publishing assets in multiple variations—a fully packaged component and individual "parts" that can be referenced into other components.

## Extensibility

The `Kind` library that ships with OpenUSD can be extended using plugin info, allowing users to define their own extensions to component, assembly, and subcomponent kinds. For example, a pipeline might want to differentiate between various levels of assemblies (such as “location” vs “world”) or types of subcomponents.

However, the rules governing model hierarchy are strict and, unlike most fields, are core to OpenUSD’s composition engine. Mixing internal taxonomies with the model hierarchy can lead to unintended complexity. Additionally, if your plugin info doesn't include your extensions, clients might struggle to interpret your kind structure or reconcile it with their own, resulting in invalid model hierarchies.

To avoid these issues, it's best to use custom properties, user properties, or {term}`schemas <Schema>` to describe your taxonomies, and rarely (if ever) expose these to the `Kind` library.

When extending the core kinds, consider using a naming convention, such as prefixing component extensions with `c_` and assembly extensions with `a_`. This practice leaves a trail for users to easily identify the core kind from an extension. As an analogy, OpenUSD requires {term}`API schemas <API Schema>` to be suffixed with API so they can be distinguished from {term}`typed schemas <IsA Schema>` just by the class name. 

---

Before we move onto our final exercises, consider the following tips when working with model hierarchies:

* Model hierarchies are structured around the traversal pruning component model boundary.   
* They should be shallow compared to the full prim hierarchy to minimize additional composition costs.   
* Model hierarchies should be consistent across different contexts.  
* Minimize usage of kind in favor of custom properties or schemas. 