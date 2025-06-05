![Value Resolution Definition](../../images/ValueResolution_Defintion.webm)

Value resolution is the algorithm by which final values for properties or metadata are compiled from all sources. The algorithm consumes an ordered list of values including default values, timeSamples, and fallback values from the composition and returns the resolved value.  

### How Does It Work?

Value resolution combines potentially many pieces of data together to produce a single value. It is distinct from composition, which caches the "indexing" of layers when a stage is opened or a new scene description is authored.

There are a few ways value resolution is distinct from composition.

Composition rules vary by composition arc, and the algorithm processes a scene’s composition arcs into an index of sites for each composed prim. Value resolution rules, on the other hand, vary by metadatum. Value resolution consumes the list of contributing sites from strongest to weakest, regardless
of the composition arcs that created the list.

Additionally, composition is cached, while value resolution is not. Composition results are cached at the prim level for fast access, but USD does not pre-compute or cache any per-composed-property information to keep memory footprint low.

### Working With Python

You can use value resolution for resolving metadata using
`UsdObject::GetMetadata`, where the general rule is that the strongest opinion wins. When resolving relationships, all opinions are combined, not just the strongest opinion.

Meanwhile, you can compute value resolution for attributes by using `UsdAttribute::Get()`.

Attribute value resolution is unique.

* For each site, value resolution checks three value sources: 
    * Value clips
    * Authored timeSamples
    * Default value, in that order
* Time offsets: Queries are affected by time-scaling operators like `SetTimeSamples`
* If time falls between samples, interpolation is performed before falling back to the earlier sample. This is how the value resolution calculates specific timeSample data 

### Key Takeaways

Value resolution allows OpenUSD to provide a rich set of composition semantics, while keeping the core lightweight and performant for random access to composed data.

For example, value resolution can be used in a product design or VFX workflow, where you often have multiple teams working on various aspects of a scene, to seamlessly combine data from multiple sources into a single model without overwriting work.

Another example can be illustrated with a robot arm model defined in two layers:

* The base layer specifies the robot arm’s default properties, such as its position `(0, 0, 0)`.
* The operational layer contains overrides for when the robot arm is in use, changing its position to `(5, 0, 0)`.

During value resolution, the final scene integrates these layers, resulting in the robot arm being positioned at `(5, 0, 0)`, reflecting its operational state while retaining unchanged attributes from the Base Layer.

Understanding value resolution is key to working effectively with OpenUSD's non-destructive data modeling capabilities.



