# OpenUSD Glossary

:::{glossary}
:sorted:

Active and Inactive

    The `active` metadata provides a way to temporarily remove a prim and its children from your scene without actually deleting them.

    By default, all prims are active—meaning they are composed onto the stage and visited during stage traversals. Deactivating a prim by setting its `active` metadata to false effectively performs a non-destructive deletion: the prim and all of its descendants are pruned from the composed stage view and excluded from traversals, but the scene description remains intact and can be reactivated by stronger layer opinions. This pruning mechanism is essential for managing scene complexity and improving performance by temporarily removing unnecessary parts of the scene graph without permanently deleting them.

    **Also Known As:** *activation, deactivation*  
    **Further Reading**: [Active and Inactive Prims](<./beyond-basics/active-inactive-prims.md>), [Active/Inactive -- OpenUSD.org](<inv:usd:std#glossary:active / inactive>)

Animated Value

    An animated value is data that changes over time rather than having a single fixed value. (e.g. time samples or animation splines)

    Attributes can store time-varying data using time samples (discrete time-value pairs) or animation splines, and USD automatically interpolates between these data points when you query an attribute at a specific time. An attribute can have both a static default value and animated values, with the animated values taking precedence when querying at specific time codes.

    **Also Known As:** *time-varying value, time-sampled value*  
    **Further Reading**: [Time Codes and Time Samples](<./stage-setting/timecodes-timesamples.md>), [Animated Value -- OpenUSD.org](<inv:usd:std#glossary:animated value>)


API Schema

    An API schema provides a collection of related properties and methods that can be applied to prims to add specific functionality.

    While IsA schemas define what a prim fundamentally "is," API schemas define what capabilities a prim "has"—they add optional behaviors and properties to already-typed prims. API schemas can be single-apply (like `UsdPhysicsRigidBodyAPI`) or multiple-apply (like `UsdCollectionAPI`, which can be applied multiple times with different instance names). API schemas typically have an "API" suffix in their class names and namespace their properties to avoid conflicts. (e.g., `UsdPhysicsRigidBodyAPI` creates attributes like `physics:velocity`)

    **Further Reading**: [API Schema -- OpenUSD.org](<inv:usd:std#glossary:api schema>), [Generating New Schemas](<https://openusd.org/release/api/_usd__page__generating_schemas.html>)

Assembly

    An assembly is a published asset that groups multiple models together into a meaningful collection.

    Assemblies are group models marked with the "assembly" kind that aggregate other models often through references, and they can themselves be published as reusable assets. This enables you to build complex scenes hierarchically by combining smaller assets into assemblies, then combining assemblies into even larger aggregations.

    **Also Known As:** *assembly asset, assembly model*  
    **Further Reading**: [Model Hierarchy](<./asset-structure/model-hierarchy/index.md>), [Assembly -- OpenUSD.org](<inv:usd:std#glossary:assembly>)

Asset

    A named resource (often versioned) that is maintained and reused (e.g. layers, textures, volumes, etc.)
    

    USD defines a specialized string type called "asset" so that all metadata and attributes that refer to assets can be quickly and robustly identified. Assets can be single files (like a texture) or a collection of files anchored by a main file that references others. The USD text format uses special syntax for asset-valued strings with the "@" symbol as delimiter (or "@@@" if the asset path itself contains "@").

    **Also Known As:** *asset path, asset reference*  
    **Further Reading**: [Asset Resolution -- OpenUSD.org](<inv:usd:std#glossary:asset resolution>), [USD Datatypes](<https://openusd.org/release/api/_usd__page__datatypes.html>)

Asset Info

    Asset info is a metadata dictionary that stores asset identification and management information on prims and properties.

    This flexible dictionary supports custom fields but includes four core fields with direct API access: identifier (the asset path), name (asset 
    database name), payloadAssetDependencies (pre-computed dependencies for optimization), and version (asset revision information). Asset info persists through composition and flattening, enabling you to track where assets are introduced in your scene and reconstruct references to them.

    **Also Known As:** *AssetInfo, asset metadata*  
    **Further Reading**: [AssetInfo -- OpenUSD.org](<inv:usd:std#glossary:assetinfo>), [UsdObject AssetInfo API](<https://openusd.org/release/api/class_usd_object.html>)

Asset Resolution

    Asset resolution is the process of translating an asset path into the actual location of a consumable resource.

    USD provides a plugin point called `ArResolver` that you can customize to resolve assets using your own logic, external databases, or version control systems. If no custom resolver is available, USD uses a default resolver that searches for assets using configurable search paths.

    **Further Reading**: [Asset Resolution -- OpenUSD.org](<inv:usd:std#glossary:asset resolution>), [ArResolver Documentation](<https://openusd.org/release/api/ar_page_front.html>)

Attribute

    An attribute is a property that holds typed data values that can vary over time or have a single default value.

    Attributes are the most common properties in USD and support various data types like float, string, and matrix. They can store both a static default value and time-varying values (via time samples or splines), with value resolution following "strongest wins" rules where the strongest prim spec determines the final value.

    **Further Reading**: [What Is an Attribute?](<./stage-setting/properties/attributes.md>), [Attribute -- OpenUSD.org](<inv:usd:std#glossary:attribute>)

Attribute Block

    An attribute block prevents an attribute from having any value by blocking all opinions from weaker layers.

    Authoring `None` with `UsdAttribute::Block()` creates a block that prevents weaker layers from contributing values, though stronger layers can still override the block itself. You can block entire attributes or specific time samples and spline segments to precisely control which values are blocked over time.

    **Also Known As:** *value block*  
    **Further Reading**: [Attribute Block -- OpenUSD.org](<inv:usd:std#glossary:attribute block>), [What Is Value Resolution?](<./beyond-basics/value-resolution.md>)

Change Processing

    Change processing is how a stage automatically updates itself when any of its contributing layers are edited.

    When you edit a layer, the stage immediately re-indexes affected prims in the same thread, potentially adding, removing, or modifying prims to maintain an accurate composed view. After processing changes, the stage notifies registered clients through the notification system so they can update themselves accordingly.

     **Further Reading**: [Change Processing -- OpenUSD.org](<inv:usd:std#glossary:change processing>), [UsdNotice](<https://openusd.org/release/api/class_usd_notice.html>)

Class

    A class is a prim specifier that creates abstract prims meant to be composed onto other prims.

    Class prims are marked as abstract and skipped by default traversals, making them ideal templates from which other prims can inherit shared properties and metadata. You typically use classes to define reusable configurations that multiple prims can inherit through the inherit composition arc. Classes can define 
    or override metadata, properties, and nested prims.

    **Also Known As:** *class prim, abstract class*  
    **Further Reading**: [What Are Specifiers?](<./composition-basics/specifiers.md>), [Class -- OpenUSD.org](<inv:usd:std#glossary:class>)

Collection

    A collection uses relationships to efficiently identify large sets of objects by including and excluding hierarchical paths.

    Collections use include and exclude relationships with expansion rules to compactly represent large object sets, implemented through the multiple-apply `UsdCollectionAPI` schema. They support explicit path lists and pattern-based membership, and can include prims, properties, or even other collections.

    **Also Known As:** *UsdCollectionAPI*  
    **Further Reading**: [Collections and Patterns](<https://openusd.org/release/user_guides/collections_and_patterns.html>), [Collection -- OpenUSD.org](<inv:usd:std#glossary:collection>)

Component

    A component is a leaf model in the USD model hierarchy that represents a complete, publishable asset.

    Components are marked with the "component" kind and represent the leaf or bottom level of the model hierarchy—complete assets like props, characters, or set pieces. They can contain subcomponents but cannot contain other models, making them the building blocks that assemblies and groups aggregate together.

    **Also Known As:** *component model, component asset*  
    **Further Reading**: [Model Hierarchy](<./asset-structure/model-hierarchy/index.md>), [Component -- OpenUSD.org](<inv:usd:std#glossary:component>)

Composition

    Composition is the process of combining multiple layers and scene graph elements together to create a final composed scene.

    USD evaluates all composition arcs (sublayers, references, payloads, variant sets, inherits, and specializes) to build the stage's scenegraph, creating indexes for each prim that enable efficient value resolution. Composition happens when opening a stage, loading or unloading prims, and whenever contributing layers are edited.

    **Also Known As:** *scene composition*  
    **Further Reading**: [Creating Composition Arcs](<./creating-composition-arcs/index.md>), [Composition -- OpenUSD.org](<inv:usd:std#glossary:composition>)

Composition Arcs

    Composition arcs are the operators that allow USD to combine multiple layers of scene description in specific ways.

    USD provides seven composition arcs—sublayer, inherit, variant set, relocate, reference, payload, and specialize—remembered by the mnemonic LIVERPS, which also represents their strength ordering. These directional operators combine layers and prim specs into an ordered graph, and all arcs except sublayers support prim name changes through path translation.

    **Also Known As:** *arcs, composition operators*  
    **Further Reading**: [Creating Composition Arcs](<./creating-composition-arcs/index.md>), [LIVERPS Strength Ordering -- OpenUSD.org](<inv:usd:std#glossary:liverps strength ordering>)

Connection

    A connection is a typed link between attributes that can represent dataflow relationships in networks like shader graphs.

    Connections are a sub-aspect of attributes that allow input attributes to target output attributes for dataflow in consuming applications. While USD itself doesn't provide dataflow behavior, schemas use connections to encode networks—particularly shading networks where nodes' inputs and outputs are linked together.

    **Also Known As:** *attribute connection*  
    **Further Reading**: [Connection -- OpenUSD.org](<inv:usd:std#glossary:connection>)

Crate File Format

    The crate file format is USD's binary file format with `.usdc` extension that is optimized for performance and file size.

    Crate files (`.usdc`) are losslessly convertible to and from the text format (`.usda`) and feature data deduplication, lockless multi-threaded reading, and low-latency lazy queries—only reading a small index on open and deferring big data until needed. This makes crate files significantly more efficient than text files, which must be fully parsed when opened.

    **Also Known As:** *.usdc, USD binary format*  
    **Further Reading**: [USD File Formats](<./stage-setting/usd-file-formats.md>), [Crate File Format -- OpenUSD.org](<inv:usd:std#glossary:crate file format>)

Def

    Def is a prim specifier that defines a prim as being present and available for processing on the stage.

    Short for "define", the def specifier indicates that a prim is concretely defined on the stage. Prims with def specifiers are present and visited by default stage traversals like rendering, making it the standard way to declare prims that actively participate in your scene.

    **Also Known As:** *define, defined prim*  
    **Further Reading**: [What Are Specifiers?](<./composition-basics/specifiers.md>), [Def -- OpenUSD.org](<inv:usd:std#glossary:def>)

Default Value

    A default value is the timeless, static value of an attribute that exists outside of time.

    Each attribute has a separate default field that you access with `UsdTimeCode::Default()`, which exists independently of animated values. While an animated value is stronger than a default within the same prim spec, a default in a stronger layer still wins over animated values in weaker layers due to composition strength ordering.

    **Also Known As:** *default, static value*  
    **Further Reading**: [Value Resolution](<./beyond-basics/value-resolution.md>), [Default Value -- OpenUSD.org](<inv:usd:std#glossary:default value>)

Direct Opinion

    A direct opinion is scene description authored directly on a prim rather than inherited through ancestral composition arcs.

    Direct opinions are authored at a prim's specific path, while indirect opinions come from composition arcs on ancestor prims. This distinction is important because direct composition arcs (like direct references) are stronger than ancestral ones (ancestral references) in value resolution. This concept applies similarly to all composition arcs except sublayers.

    **Further Reading**: [Direct Opinion -- OpenUSD.org](<inv:usd:std#glossary:direct opinion>)

Fallback

    A fallback is a default value defined by a schema that applies when no value has been explicitly authored.

    Schemas define fallback values for their attributes to provide sensible defaults when nothing is authored, keeping scene description sparse and compact. For example, `UsdGeomImageable` visibility has a fallback of "inherited" and `UsdGeomGprim` orientation has a fallback of "rightHanded", so you only need to author these attributes when you want non-default values.

    **Also Known As:** *schema fallback, default fallback*  
    **Further Reading**: [Fallback -- OpenUSD.org](<inv:usd:std#glossary:fallback>)

Flatten

    Flattening is the process of baking all composition arcs into a single self-contained layer.

    Flattening converts a dynamically composed stage into a single standalone layer by resolving all composition arcs and baking the results, creating a highly portable file that contains everything. The trade-off is larger file size since referenced assets get duplicated, and the process can be memory and compute intensive. You can flatten using `UsdStage::Flatten` or the usdcat tool with `--flatten`.

    **Further Reading**: [Flatten -- OpenUSD.org](<inv:usd:std#glossary:flatten>), [usdcat Tool](<https://openusd.org/release/toolset.html#usdcat>)

Gprim

    Gprim (geometric primitive) is the base type for all renderable geometric primitives in UsdGeom.

    Gprims inherit from `UsdGeomGprim` and represent actual renderable geometry like meshes, curves, points, and volumes, with common attributes for rendering such as `doubleSided`, `orientation`, and `purpose`. UsdGeom provides a rich set of gprim types including `UsdGeomMesh`, `UsdGeomCurves`, `UsdGeomPoints`, and various geometric volumes.

    **Also Known As:** *geometric primitive*  
    **Further Reading**: [UsdGeom Documentation](<https://openusd.org/release/api/usd_geom_page_front.html>), [Gprim -- OpenUSD.org](<inv:usd:std#glossary:gprim>)

Group

    Group is a kind of model that contains other models, forming collections of models in the model hierarchy.

    Group models serve as containers that can have other model children (unlike component models which are leaves), with assemblies being a specific type of group. This creates a clear organizational structure where only group models can contain other models, forming hierarchical aggregations of scene elements.

    **Also Known As:** *group model*  
    **Further Reading**: [Model Hierarchy](<./asset-structure/model-hierarchy/index.md>), [Group -- OpenUSD.org](<inv:usd:std#glossary:group>)

Hydra

    Hydra is USD's high-performance rendering architecture that provides an abstraction layer between scene data and renderers.

    Hydra enables multiple renderers—from real-time OpenGL/Vulkan to production raytracers—to operate on USD scenes through a common interface using a scene delegation system with efficient change tracking and update mechanisms. This architecture powers usdview's visualization and allows applications to swap rendering backends without modifying scene description.

    **Further Reading**: [Hydra Overview](<./beyond-basics/hydra.md>), [Hydra -- OpenUSD.org](<inv:usd:std#glossary:hydra>)

Index

    An index is the composition structure that determines how a prim is constructed from multiple prim specs.

    Each composed prim has an index computed during composition that maps it to all contributing prim specs across layers, creating an ordered graph that USD traverses to resolve property and metadata values. While you can examine a prim's index for debugging, most high-level USD operations handle index traversal automatically.

    **Also Known As:** *PrimIndex, prim index, composition index*  
    **Further Reading**: [Index -- OpenUSD.org](<inv:usd:std#glossary:index>)

Inherit
    
    Inherits is a composition arc that allows prims to inherit scene description from a prim, enabling context-specific modifications to the inherited source to broadcast to all inheriting prims within the same layer stack.

    When a prim establishes an inherit arc, it gains all properties, metadata, and nested hierarchy from the source prim (typically a class prim). The key difference from references is that inherits allow modifications to the source prim to be broadcast to all inheriting prims within the same layer stack context, while references create isolated copies. This enables context-specific overrides—changes made in one layer stack don't affect other layer stacks—making inherits ideal for applying variations to all instances of an asset within a particular scene without affecting the asset globally. It is also a useful mechanism for refining scengraph instances.

    **Also Known As:** *inherits, inherit arc*  
    **Further Reading**: [Inherits and Specializes](<./creating-composition-arcs/inherits-specializes/index.md>), [Inherits -- OpenUSD.org](<inv:usd:std#glossary:inherits>)

Instanceable

    Instanceable is metadata that marks a prim as eligible for scenegraph instancing to share composed data in memory.

    Marking a prim instanceable with `UsdPrim::SetInstanceable(true)` allows USD to share the composed prim index and attribute values across all instances with identical composition structure. This provides significant memory savings when the same asset is referenced many times in a scene. Scenegraph instancing is transparent to most queries, though you can detect instances with `UsdPrim::IsInstance()` and access prototypes with `UsdPrim::GetPrimInPrototype()`.

    **Also Known As:** *instanceable metadata*  
    **Further Reading**: [What Is Instancing?](<./asset-modularity-instancing/what-is-instancing.md>), [Instanceable -- OpenUSD.org](<inv:usd:std#glossary:instanceable>)

Instancing

    Instancing is USD's memory-sharing mechanism for efficiently handling multiple copies of the same composed prim structure.

    USD provides two instancing implementations: scenegraph instancing, which shares composed prim structures (implicit prototypes) across multiple explicit instances with identical composition arcs, and point instancing, which uses the PointInstancer schema to efficiently represent massive numbers of instances through array attributes. Scenegraph instancing allows per-instance overrides on the instanceable prim itself, while point instancing requires full array authoring for any changes.

    **Also Known As:** *scene instancing, shared instancing*  
    **Further Reading**: [Asset Modularity and Instancing](<./asset-modularity-instancing/index.md>), [Instancing -- OpenUSD.org](<inv:usd:std#glossary:instancing>)

Interpolation

    Interpolation determines how values are calculated between discrete authored data points and carries distinct meanings for temporal data and geometric attributes.

    Interpolation can refer to one of two distint concepts—temporal interpolation affects animation over time, while spatial interpolation affects attribute distribution across surface topology. For **temporal interpolation**, this applies to time samples and spline animation. USD calculates values between time samples using methods like linear (straight line between values) and held (value stays constant until next sample). Animation splines use curve-based interpolation (using Bezier or Hermite curves). For **spatial interpolation**, interpolation describes how primvar values vary across a primitive's surface using modes like constant (one value for entire primitive), uniform (one value per face), vertex (one value per vertex), or faceVarying (one value per face-vertex). 

    **Also Known As:** *temporal interpolation, geometric interpolation, spatial interpolation*  
    **Further Reading**: [Time Codes and Time Samples](<./stage-setting/timecodes-timesamples.md>), [Primvars](<./beyond-basics/primvars.md>)

IsA Schema

    An IsA schema defines what type of thing a prim fundamentally is, determining its core identity and built-in properties.

    IsA schemas (also called typed schemas) define a prim's fundamental type through the `typeName` metadata, with each prim having only one IsA schema that determines its core nature—like Mesh, Camera, or Light. All UsdGeom primitives like `UsdGeomMesh` and `UsdGeomSphere` are IsA schemas that provide a prim's essential attributes and behaviors.

    **Also Known As:** *typed schema, prim type, type schema*  
    **Further Reading**: [Schemas](<./scene-description-blueprints/schemas.md>), [IsA Schema -- OpenUSD.org](<inv:usd:std#glossary:isa schema>)

Kind

    Kind is metadata that classifies prims into categories for organizational and traversal purposes.

    USD provides the core kinds including "model" (abstract base), "component" (leaf models), "group" (container models), and "assembly" (publishable aggregates). Additonally, you can extend the kind system with custom kinds derived from the core ones.

    **Also Known As:** *prim kind, model kind*  
    **Further Reading**: [Model Kinds](<./beyond-basics/model-kinds.md>), [Kind -- OpenUSD.org](<inv:usd:std#glossary:kind>)

Layer

    A layer is a container that stores USD scene description, typically backed by a file on disk.

    Layers contain prim specs, properties, metadata, and composition arcs, and can be files in `.usd`, `.usda` (text), or `.usdc` (binary) format, or exist only in memory. Multiple layers combine through composition arcs to create the final composed stage, making layers the fundamental unit of USD composition (represented by the `SdfLayer` class).

    **Also Known As:** *USD layer, scene layer, SdfLayer*  
    **Further Reading**: [What Are Layers?](<./composition-basics/layers.md>), [Layer -- OpenUSD.org](<inv:usd:std#glossary:layer>)

Layer Offset

    A layer offset adjusts time values when composing layers through sublayers, references, or payloads.

    Layer offsets use an offset value (added to time codes) and a scale value (multiplies time codes) to retime animated data non-destructively during composition, following the formula `scaledTime = (time * scale) + offset`. This lets you adjust when animations start or their playback speed without modifying source layers.

    **Also Known As:** *layer time offset*  
    **Further Reading**: [Layer Offset -- OpenUSD.org](<inv:usd:std#glossary:layer offset>)

Layer Stack

    A layer stack is an ordered list of sublayers combined to form a single namespace for composition.

    Starting from a root layer, USD recursively gathers all sublayers into a layer stack where stronger (earlier) sublayers override weaker (later) ones. Layer stacks are the fundamental units that composition arcs like references and payloads target, with each layer stack maintaining its own namespace and optional session layer for interactive overrides.

    **Also Known As:** *LayerStack, layer stack*  
    **Further Reading**: [Sublayers](<./creating-composition-arcs/sublayers/index.md>), [LayerStack -- OpenUSD.org](<inv:usd:std#glossary:layerstack>)

List Editing

    A system for sparsely combining ordered lists from multiple layers using operations like prepend, append, delete, and reset to explicit.

    USD provides list editing operations including prepend, append, delete, and reset to explicit that allow each layer to non-destructively modify lists like composition arcs, relationships, and variant sets. This enables multiple layers to contribute to the same list, with each layer able to add, remove, or completely replace items. List editing follows strength ordering rules where stronger layers' operations take precedence over weaker ones.

    **Also Known As:** *list ops, sparse lists, SdfListOp*  
    **Further Reading**: [List Editing -- OpenUSD.org](<inv:usd:std#glossary:list editing>)

LIVERPS Strength Ordering

    LIVERPS is the mnemonic for USD's composition strength ordering: local (sublayers), inherits, variant sets, relocates, references, payloads, specializes.

    This acronym defines the strength hierarchy from strongest to weakest: local opinions (including sublayers), inherits, variant sets, relocates, references, payloads, and specializes. Within each category, direct arcs are stronger than ancestral arcs, and this ordering determines which opinion wins during value resolution.

    **Also Known As:** *strength ordering, composition strength, LIVRPS*  
    **Further Reading**: [Strength Ordering](<./creating-composition-arcs/strength-ordering/index.md>), [LIVERPS -- OpenUSD.org](<inv:usd:std#glossary:liverps strength ordering>)

Load and Unload

    Loading and unloading controls which payload arcs are traversed during composition.

    Payload arcs can be lazy loaded. When opening a stage with `UsdStage::InitialLoadSet::LoadNone`, payload arcs are recorded but not traversed, allowing you to construct a working set by loading only needed prims using `UsdPrim::Load()`. You can also unload previously loaded prims with `UsdPrim::Unload()`. This provides scalability for large scenes by allowing you to work with a subset of the full scene description.

    **Also Known As:** *payload loading*  
    **Further Reading**: [What Are Payloads?](<./creating-composition-arcs/references-payloads/what-are-payloads.md>), [Load and Unload -- OpenUSD.org](<inv:usd:std#glossary:load / unload>)

Metadata

    Metadata is data about prims and properties that guides USD's behavior but is not renderable scene content.

    Metadata includes information like `kind`, `active`, `instanceable`, `documentation`, `assetInfo`, and composition arc lists. Unlike properties (attributes and relationships), metadata does not vary over time and is accessed through special API rather than as properties. Metadata can be defined by schemas or added as custom metadata, and participates in composition through its own resolution rules.

    **Also Known As:** *prim metadata, property metadata, layer metadata*  
    **Further Reading**: [Metadata](<./stage-setting/metadata.md>), [Metadata -- OpenUSD.org](<inv:usd:std#glossary:metadata>)

Model

    Models partition large scenegraphs into manageable pieces by annotating prims with kind metadata

    Models create a hierarchy that acts as a table of contents for important subtrees. The core model kinds are "component" (leaf models representing complete assets) and the aggregating kinds "group" and "assembly" (models that contain other models), enabling efficient traversal and queries through the UsdPrim API.

    **Also Known As:** *model prim, model kind*  
    **Further Reading**: [Model Hierarchy](<./asset-structure/model-hierarchy/index.md>), [Model -- OpenUSD.org](<inv:usd:std#glossary:model>)

Model Hierarchy

    The model hierarchy is a organizational system that creates a table of contents of important subtrees in a scene.

    Model hierarchy is a contiguous prefix of the scenegraph that acts as a table of contents for important subtrees, built from prims with model kinds that follow strict containment rules: only group models (group or assembly) can contain other models, and a prim can only be a model if its parent is also a group model (except the root). This self-assembling index structure aligns closely with referenced assets, enabling efficient discovery and traversal of major scene components without needing to dive into the full prim hierarchy.

    **Further Reading**: [Model Hierarchy](<./asset-structure/model-hierarchy/index.md>), [Model Hierarchy -- OpenUSD.org](<inv:usd:std#glossary:model hierarchy>)

Namespace

    Namespace is the term USD uses for the hierarchical tree structure of prim paths that organize a stage or layer.

    On a stage, namespace consists of all the prim paths that provide identities for prims, organized as a tree with a pseudo-root at the top. Paths in the namespace use forward slashes like file paths (e.g., `/World/Characters/Hero`). Properties also have namespaced names within their containing prim, allowing for organized grouping of related properties like `inputs:diffuseColor` or `primvars:st`.

    **Also Known As:** *scene hierarchy, prim hierarchy, scene graph namespace*  
    **Further Reading**: [Prim and Property Paths](<./stage-setting/prim-property-paths.md>), [Namespace -- OpenUSD.org](<inv:usd:std#glossary:namespace>)

Opinions

    Opinions are the atomic elements of scene description that participate in value resolution.

    Each time you author a value for a metadatum, attribute, or relationship, you're expressing an opinion in a prim spec in a layer. On a composed stage, any object may be affected by multiple opinions from different layers, with the ordering determined by LIVERPS strength ordering. Value resolution selects the strongest opinion from all contributing opinions to determine the final composed value.

    **Also Known As:** *authored opinions*  
    **Further Reading**: [Value Resolution](<./beyond-basics/value-resolution.md>), [Opinions -- OpenUSD.org](<inv:usd:std#glossary:opinions>)

Over

    Over is a prim specifier that creates speculative override containers without defining new prims.

    Over is short for override. An over is the weakest specifier, letting you author opinions that contribute to existing prims without asserting the prim's existence. If all contributing specs are overs, the prim won't appear in default traversals. Overs are ideal for sparse overrides in layers that modify existing compositions without defining new scene structure.

    **Also Known As:** *override*  
    **Further Reading**: [Specifiers](<./composition-basics/specifiers.md>), [Over -- OpenUSD.org](<inv:usd:std#glossary:over>)

Path

    A path is a location identifier in USD's namespace, represented by the SdfPath class.

    Paths use forward-slash syntax like file paths (e.g., `/Root/Child/Grandchild`) and can identify prims, properties, or even content within variant sets. Absolute paths start with `/`, and properties are accessed with a dot (e.g., `/Prim.attribute`). SdfPath is a compact, thread-safe key used throughout USD APIs for fetching and storing scene description, and the syntax supports variant selections and other composition concepts.

    **Also Known As:** *prim path, property path, SdfPath*  
    **Further Reading**: [Prim and Property Paths](<./stage-setting/prim-property-paths.md>), [Path -- OpenUSD.org](<inv:usd:std#glossary:path>)

Path Translation

    Path translation is the automatic remapping of paths that happens when composition arcs rename prims.

    All composition arcs except sublayers allow prim name changes as the source prim gets composed under the destination prim. The stage automatically applies path translation so users work in the fully composed namespace rather than worrying about the original namespaces in individual layers. Path translation occurs when querying prims and relationship targets, and inverse translation happens when authoring through EditTargets.

    **Also Known As:** *path remapping*  
    **Further Reading**: [Path Translation -- OpenUSD.org](<inv:usd:std#glossary:path translation>), [References](<./creating-composition-arcs/references-payloads/index.md>)

Payload

    A payload is a composition arc similar to references but with deferred loading for scalability.

    Payloads act like references but are recorded without traversing when you open a stage with `LoadNone`, letting you control which parts of large scenes load like in working sets. Payloads are also weaker than references in LIVERPS ordering, and are typically added to component asset root prims for efficient scalable composition.

    **Also Known As:** *payload arc*  
    **Further Reading**: [What Are Payloads?](./creating-composition-arcs/references-payloads/what-are-payloads.md), [Reference/Payload Pattern](<./asset-structure/reference-payload-pattern/index.md>), [Payload -- OpenUSD.org](<inv:usd:std#glossary:payload>)

Prim

    A prim (primitive) is the primary container object in USD that can hold other prims and properties.

    Prims create a namespace hierarchy on a stage and contain ordered properties (attributes and relationships) that hold meaningful data. Prims always have a resolved specifier (def, over, or class) that determines their role, and may have a schema typeName that dictates what data they contain. Prims provide the granularity for instancing, load/unload behavior, and activation/deactivation. The `UsdPrim` class provides the API for interacting with prims.

    **Also Known As:** *primitive, scene primitive, UsdPrim*  
    **Further Reading**: [What Are Prims?](<./stage-setting/prims.md>), [Prim -- OpenUSD.org](<inv:usd:std#glossary:prim>)

Prim Definition

    A prim definition is the set of built-in properties and metadata a prim gains from its type and applied API schemas.

    The prim definition combines a prim's IsA schema and applied API schemas to determine its built-in properties and metadata beyond its authored scene description. It also provides fallback values for these built-in elements during value resolution, accessible through the `UsdPrimDefinition` class.

    **Also Known As:** *type definition, schema definition*  
    **Further Reading**: [Prim Definition -- OpenUSD.org](<inv:usd:std#glossary:prim definition>), [UsdPrimDefinition API](<https://openusd.org/release/api/class_usd_prim_definition.html>)

Prim Spec

    A prim spec is an uncomposed prim in a layer that contributes scene description to a composed prim.

    Each composed prim on a stage is the result of potentially many prim specs each contributing their own opinions. A prim spec is a container for property data, nested prim specs, and composition arcs. Prim specs are where composition arcs are authored, and arcs that specify targets are targeting other prim specs. The `SdfPrimSpec` class represents prim specs in layers.

    **Also Known As:** *PrimSpec, prim specification*  
    **Further Reading**: [What Is Prim Composition?](<./creating-composition-arcs/prim-composition.md>), [PrimSpec -- OpenUSD.org](<inv:usd:std#glossary:primspec>)

Prim Stack

    A prim stack is the ordered list of prim specs that contribute opinions for a composed prim's metadata.

    Available through `UsdPrim::GetPrimStack()`, the prim stack is condensed from the prim's index and shows all prim specs across layers contributing to metadata. It's useful for debugging to understand which layers contribute to a prim's metadata.

    **Also Known As:** *PrimStack, prim composition stack*  
    **Further Reading**: [PrimStack -- OpenUSD.org](<inv:usd:std#glossary:primstack>)

Primvar

    A primvar (primitive variable) is a special kind of attribute that can vary and interpolate across a geometric primitive.

    Primvars use interpolation modes (constant, uniform, vertex, faceVarying, etc.) to define how values vary across a primitive's surface or volume, providing  data for shaders and other consumers. You work with primvars through `UsdGeomImageable` and `UsdGeomPrimvar`, with all primvars using the "primvars:" namespace prefix.

    **Also Known As:** *primitive variable*  
    **Further Reading**: [What Are Primvars?](<./beyond-basics/primvars.md>), [Primvar -- OpenUSD.org](<inv:usd:std#glossary:primvar>)

Property

    Properties are namespace objects that contain the actual data in USD, either as attributes or relationships.

    There are two types of properties: attributes (which hold typed data values) and relationships (which hold target paths to other objects). Properties can be ordered within their containing prim using `UsdPrim::SetPropertyOrder()` and can host metadata. Properties can also be organized into nested namespaces like `material:binding` or `primvars:displayColor` for better organization without introducing new prim containers.

    **Also Known As:** *prim property, UsdProperty*  
    **Further Reading**: [Properties](<./stage-setting/properties/index.md>), [Property -- OpenUSD.org](<inv:usd:std#glossary:property>)

Property Spec

    A property spec contains the data for a property within a layer.

    Property specs are nested inside prim specs and can contain a property's type declaration, metadata, and values. For attributes, a property spec can contain three independent values: a timeless default value, a spline, and a collection of time samples. For relationships, a property spec contains the targets as an `SdfListOp<SdfPath>`. Multiple property specs across layers combine during composition to create the final property values.

    **Also Known As:** *PropertySpec, property specification*  
    **Further Reading**: [PropertySpec -- OpenUSD.org](<inv:usd:std#glossary:propertyspec>)

Property Stack

    A property stack is the ordered list of property specs that contribute values or metadata for a composed property.

    Available through `UsdProperty::GetPropertyStack()`, the property stack should only be used for debugging, not value resolution. In the presence of value clips, the stack may need recomputation each frame, and it doesn't contain the correct time-offsets for animated values when layer offsets are present. For optimized repeated value resolution, use `UsdAttributeQuery` instead.

    **Also Known As:** *PropertyStack, property composition stack*  
    **Further Reading**: [Value Resolution](<./beyond-basics/value-resolution.md>), [PropertyStack -- OpenUSD.org](<inv:usd:std#glossary:propertystack>)

Proxy

    Proxy is a purpose value for lightweight geometry used as a placeholder for complex render geometry.

    In UsdGeom, "proxy" is one of the possible purpose values a prim can have, paired with a corresponding "render" prim. The proxy provides lightweight gprims that are cheap to load and draw, giving a preview of what the full render geometry will look like. Using proxy purpose rather than variant sets for LOD allows both proxy and render geometry to be present simultaneously, so you can quickly inspect lightweight versions while maintaining access to full-quality data.

    **Also Known As:** *proxy purpose*  
    **Further Reading**: [Purpose -- OpenUSD.org](<inv:usd:std#glossary:purpose>), [Proxy -- OpenUSD.org](<inv:usd:std#glossary:proxy>)

Pseudo-Root

    The pseudo-root is a convenience prim at path `/` that serves as the parent of all root prims on a stage.

    Each stage contains a pseudo-root prim that allows the stage to contain a single tree of prims rather than a forest. The pseudo root facilitates traversal and processing by providing a common ancestor for all authored root prims. It's represented by the path `/` and is accessible via `UsdStage::GetPseudoRoot()`.

    **Also Known As:** *PseudoRoot, root prim*  
    **Further Reading**: [Namespace -- OpenUSD.org](<inv:usd:std#glossary:namespace>), [PseudoRoot -- OpenUSD.org](<inv:usd:std#glossary:pseudoroot>)

Purpose

    Purpose is an attribute used to classify geometry into selective visibility categories.

    Purpose is a UsdGeomImageable attribute that provides visibility categories that gate scenegraph traversals, with values including "default" (general geometry), "render" (final quality), "proxy" (lightweight preview), and "guide" (visualization helpers). This allows clients to independently include or exclude geometry categories during traversals like rendering or bounding box computation. Purpose is inherited down the namespace hierarchy until explicitly overridden.

    **Further Reading**: [Purpose -- OpenUSD.org](<inv:usd:std#glossary:purpose>), [UsdGeomImageable](<https://openusd.org/release/api/class_usd_geom_imageable.html>)

Reference

    A reference is a way to graft and reuse content from another USD layer into your current layer, like linking to an external file so its contents appear in 
    your stage.

    References are a type of composition arc that copy the namespace or prim hierarchy of the referenced file into the referencing prim, allowing you to build complex scenes from modular assets. The referencing layer can apply overrides on top of the referenced content, following USD's strength ordering rules where opinions closer to the root are stronger. This enables non-destructive workflows where the same asset can be referenced multiple times with different variations without modifying the original source file.

    **Also Known As:** *reference arc, prim reference*  
    **Further Reading**: [What Are References?](<./creating-composition-arcs/references-payloads/what-are-references.md>), [References -- OpenUSD.org](<inv:usd:std#glossary:references>)

Relationship

    A relationship is a property that establishes pointers or links between prims and properties in the scene hierarchy.

    Relationships are typeless properties that store lists of paths to other objects, with USD automatically translating paths through composition. They're independent properties (unlike connections which are tied to attributes) used for material bindings, collections, and other object-to-object targeting, with list-editing support for collaborative authoring.

    **Further Reading**: [What Are Relationships?](<./stage-setting/properties/relationships.md>), [Relationship -- OpenUSD.org](<inv:usd:std#glossary:relationship>)

Relocate

    Relocate is a composition arc that non-destructively remaps prim paths introduced through composition.

    Defined in layer metadata, relocates map source paths to target paths, allowing you to rename or reparent prims introduced via ancestral composition arcs without modifying the source. This is useful when you need to restructure composed prims but can't edit them directly because they come from references or other arcs. Relocates are stronger than references but weaker than variants in LIVERPS strength ordering.

    **Also Known As:** *relocates, relocate arc*  
    **Further Reading**: [Relocates -- OpenUSD.org](<inv:usd:std#glossary:relocates>)

Root Layer Stack

    The root layer stack is the layer stack formed by the root layer, its sublayers, and the session layer of a stage.

    Every stage has a root layer stack combining the root layer's sublayers with the session layer.The root layer stack is special because prims declared in root layers are locatable using the same paths as composed prims on the stage, and it's where EditTargets can operate. This facilitates collaborative workflows where different departments author in separate sublayers.

    **Also Known As:** *Root LayerStack*  
    **Further Reading**: [LayerStack -- OpenUSD.org](<inv:usd:std#glossary:layerstack>), [Root LayerStack -- OpenUSD.org](<inv:usd:std#glossary:root layerstack>)

Schema

    A schema is an object that provides structured API for authoring and retrieving data from prims or properties.

    Schemas are lightweight wrappers around UsdObjects (typically prims, but also properties) that provide structured APIs, coming in two types: IsA schemas (defining prim types) and API schemas (adding functionality). USD organizes schemas into families like UsdGeom for geometry and UsdShade for shading, with code generation tools available for creating custom schemas.

    **Also Known As:** *USD schema, prim schema*  
    **Further Reading**: [What Are Schemas?](<./scene-description-blueprints/schemas.md>), [Schema -- OpenUSD.org](<inv:usd:std#glossary:schema>)

Session Layer

    The session layer provides scratch space for interactive overrides and experiments without modifying asset files.

    Created optionally with a stage, the session layer is the strongest layer in the stage's root layer stack and can have its own sublayers. Session layers embody application state rather than asset data, and commonly contain UI-driven selections like variant choices, visibility overrides, and activation state. `UsdStage::Save()` does not save the session layer, as it's considered temporary application state rather than permanent scene data.

    **Further Reading**: [Session Layer -- OpenUSD.org](<inv:usd:std#glossary:session layer>), [usdview](<https://openusd.org/release/toolset.html#usdview>)

Specialize

    Specializes is a composition arc that broadcasts fallback values from a source prim, applying only to specializing prims that don't have their own authored opinion for a given spec.

    Similar to inherits, specializes allows modifications to the source prim to broadcast across layer stacks, but unlike inherits, these act as fallback values—they only apply when there isn't another authored opinion on the target prim. This mirrors traditional object-oriented programming inheritance, where objects that override class members ignore updates to those members, while objects still using class-defined values automatically reflect changes. Specializes is the weakest composition arc in LIVERPS ordering, ensuring that any directly authored opinion on a specialized prim always wins.

    **Also Known As:** *specializes, specialize arc*  
    **Further Reading**: [Inherits and Specializes](<./creating-composition-arcs/inherits-specializes/index.md>), [Specializes -- OpenUSD.org](<inv:usd:std#glossary:specializes>)

Specifier

    A specifier conveys the author's intent for how a prim spec should be interpreted in composition.

    The three specifiers are def (defines concrete prims), over (provides speculative overrides), and class (creates abstract prims for inheritance), with a prim's resolved specifier determining traversal visibility. Default traversals visit only defined, non-abstract prims, making specifiers fundamental to controlling prim renderability and composition behavior.

    **Also Known As:** *prim specifier, SdfSpecifier*  
    **Further Reading**: [What Are Specifiers?](<./composition-basics/specifiers.md>), [Specifier -- OpenUSD.org](<inv:usd:std#glossary:specifier>)

Stage

    A stage is a fully composed scenegraph.

    The stage always presents a composed view of scene description, managing prim composition, value resolution, and change processing. A stage is created by opening a root layer and composing all referenced/layered files it specifies. Stages provide the primary API for querying and authoring USD data through UsdPrim and UsdProperty objects. Multiple stages can be open simultaneously, and stages support both read-only and editable modes.

    **Also Known As:** *UsdStage, composed scene, scene graph*  
    **Further Reading**: [What Is a Stage?](<./stage-setting/stage.md>), [Stage -- OpenUSD.org](<inv:usd:std#glossary:stage>)

Stage Traversal

    Stage traversal is the process of visiting prims on a stage in a specific order for processing.

    USD offers configurable traversal types using predicate flags to visit all prims, only defined prims, only active prims, or custom combinations—with the default traversal visiting only defined, non-abstract, active prims. You can traverse using `UsdStage::Traverse()`, iterators, or range-based for loops, which is critical for efficient scene processing in rendering and export operations.

    **Further Reading**: [What Is Stage Traversal?](<./beyond-basics/stage-traversal.md>), [Stage Traversal -- OpenUSD.org](<inv:usd:std#glossary:stage traversal>)

Subcomponent

    A subcomponent is a prim with "subcomponent" kind that exists within a component model.

    Subcomponents represent parts of a component model that are too significant to be regular prims but aren't independent models. Subcomponent is a non-model kind. It does not inherit from model.

    **Further Reading**: [Model Kinds](<./beyond-basics/model-kinds.md>), [Subcomponent -- OpenUSD.org](<inv:usd:std#glossary:subcomponent>)

Sublayer

    Sublayer is the composition arc that combines multiple layers into an ordered stack with shared namespace in an include fashion.

    Sublayers are authored in a layer's metadata and create a layer stack where earlier (stronger) layers' opinions override later (weaker) layers' opinions. Unlike other composition arcs, sublayers don't allow prim name changes or target specific prims - they simply combine entire layers. Sublayers are the "L" in LIVERPS and are fundamental to USD's layered workflow, enabling non-destructive collaboration where different layers contribute to the same scene.

    **Also Known As:** *sublayer arc, subLayer*  
    **Further Reading**: [Sublayers](<./creating-composition-arcs/sublayers/index.md>), [SubLayers -- OpenUSD.org](<inv:usd:std#glossary:sublayers>)

Time Code

    A time code represents a point in time for querying or authoring time-varying data in USD.

    Time codes (via `UsdTimeCode`) can be numeric for specific time points or the special `UsdTimeCode::Default()` for timeless default values. Time codes serve as keys for time sample data and inputs for querying animated attributes. Stage-level time code mapping can be configured to support different temporal units and frame rate conversions.

    **Further Reading**: [Time Codes and Time Samples](<./stage-setting/timecodes-timesamples.md>), [TimeCode -- OpenUSD.org](<inv:usd:std#glossary:timecode>)

Time Sample

    A time sample is a time-value pair that defines an attribute's value at a specific time.

    Time samples are the most common way to author animated values in USD, stored as an ordered collection of time code and value pairs. When querying an attribute at a time code that doesn't exactly match an authored time sample, USD uses interpolation (linear by default) between neighboring samples. Multiple time samples can be authored efficiently and sparsely, with USD automatically handling interpolation and temporal queries.

    **Further Reading**: [Time Codes and Time Samples](<./stage-setting/timecodes-timesamples.md>), [TimeSample -- OpenUSD.org](<inv:usd:std#glossary:timesample>)

Value Clips

    Value clips is a composition feature that efficiently handles large amounts of time-varying data by referencing external time-sampled layers.

    Value clips allow you to reference time-sampled attribute values from a sequence of external layers without composing their entire structure. This is useful for simulation caches, animation data, and other large time-varying datasets. Clips metadata defines the file sequence, time mappings, and which attributes use clips. USD stitches together the clips transparently during value resolution.

    **Also Known As:** *clips, animation clips*  
    **Further Reading**: [Value Clips -- OpenUSD.org](<inv:usd:std#glossary:value clips>), [Value Clips Documentation](https://openusd.org/release/api/_usd__page__value_clips.html)

Value Resolution

    Value resolution is the process of determining the final composed value for a property or metadata from all contributing opinions.

    When querying attributes, USD traverses the composition index in strength order to find the strongest opinion, evaluating defaults, time samples, splines, blocks, and connections according to LIVERPS. Value resolution also handles interpolation for animated values and applies layer offsets from composition arcs. USD also has unique algorithms for resolving relationships and metadata values.

    **Further Reading**: [What Is Value Resolution?](<./beyond-basics/value-resolution.md>), [Value Resolution -- OpenUSD.org](<inv:usd:std#glossary:value resolution>)

Variability

    Variability defines whether a property's value is allowed to change over time.

    Attributes can have variability set to either "varying" (can change over time via time samples or splines) or "uniform" (constant over time, only default values allowed). Uniform variability is a promise that the value won't change, allowing optimizations in consumers. Relationships are always uniform as they cannot vary over time. Variability is specified when creating properties and enforced by the USD API.

    **Also Known As:** *attribute variability*  
    **Further Reading**: [Properties](<./stage-setting/properties/index.md>), [Variability -- OpenUSD.org](<inv:usd:std#glossary:variability>)

Variant

    A variant is one possible option within a variant set, allowing switchable variations of scene description.

    Variants contain complete scene description for one variation of a prim and its descendants. Only one variant from a variant set is active at a time (determined by the variant selection), and that variant's opinions participate in composition. Variants enable non-destructive alternatives like different geometries, material variations, or configuration options without duplicating the entire asset.

    **Further Reading**: [What Are Variant Sets?](<./creating-composition-arcs/variant-sets/what-are-variant-sets.md>), [Variant -- OpenUSD.org](<inv:usd:std#glossary:variant>)

Variant Set

    A Variant Set is a composition arc that provides switchable alternatives for a prim and its descendants.

    Variant Sets contain named variants (options), with one variant selected at a time to contribute to composition. A prim can have multiple variant sets for different types of variations (modeling, shading, etc.), and variant dets can be nested. Selections are typically stored in stronger layers or the session layer, allowing interactive switching. Variant dets are the "V" in LIVERPS strength ordering.

    **Also Known As:** *VariantSet, variant set arc*  
    **Further Reading**: [What Are Variant Sets?](<./creating-composition-arcs/variant-sets/what-are-variant-sets.md>), [VariantSet -- OpenUSD.org](<inv:usd:std#glossary:variantset>)

Visibility

    Visibility is a computed attribute that determines whether a prim's geometry should be rendered or displayed.

    Managed by the `UsdGeomImageable` schema, visibility is inherited down the prim hierarchy and can be set to "inherited" (use parent's visibility) or "invisible" (hide this prim and descendants). Unlike active/inactive which affects composition, visibility is purely a rendering concept. Computing visibility requires traversing ancestor prims, so USD provides the efficient `UsdGeomImageable::ComputeVisibility()` method rather than simple attribute queries.

    **Also Known As:** *prim visibility*  
    **Further Reading**: [Visibility -- OpenUSD.org](<inv:usd:std#glossary:visibility>), [UsdGeomImageable](<https://openusd.org/release/api/class_usd_geom_imageable.html>)

:::

