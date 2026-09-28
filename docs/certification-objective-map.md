# Certification Objective Map

This page maps the [OpenUSD Development Professional certification](https://www.nvidia.com/en-us/learn/certification/openusd-development-professional/) exam blueprint to the lessons in this curriculum, so you can see which objectives Learn OpenUSD prepares you for and which ones you'll need to study elsewhere.

Learn OpenUSD is designed as a foundation for the exam, not as complete exam preparation. Use this map to plan the rest of your study: work through the lessons listed for each objective, then fill the remaining gaps with the [certification study guide](https://nvdam.widen.net/s/6kxsqcsrrw/ncp-openusd-development-study-guide) and the resources on the [OpenUSD Cheatsheet](./openusd-cheatsheet.md).

```{note}
Exam topics and weightings on this page are quoted from the public [exam page](https://www.nvidia.com/en-us/learn/certification/openusd-development-professional/), last verified 2026-09-15. NVIDIA may revise the blueprint; always confirm against the official exam page before relying on it.
```

## How to Read This Page

Each objective is rated against the curriculum:

| Status | Meaning |
|---|---|
| **Covered** | Lessons teach the objective directly, with examples or exercises. |
| **Partial** | The curriculum introduces the objective but doesn't go deep enough to rely on alone. |
| **Gap** | No lesson covers this. Study it from external resources. |

## Coverage at a Glance

| Exam topic | Weight | Coverage |
|---|---|---|
| [Composition](#composition-23) | 23% | **Covered** |
| [Data Exchange](#data-exchange-15) | 15% | **Covered** |
| [Pipeline Development](#pipeline-development-14) | 14% | **Partial** |
| [Data Modeling](#data-modeling-13) | 13% | **Covered** |
| [Debugging and Troubleshooting](#debugging-and-troubleshooting-11) | 11% | **Partial** |
| [Content Aggregation](#content-aggregation-10) | 10% | **Covered** |
| [Visualization](#visualization-8) | 8% | **Partial** |
| [Customizing USD](#customizing-usd-6) | 6% | **Gap** |

## Composition (23%)

> Author, design with, and debug composition arcs. A developer needs to know all of the composition arcs, how they work, and when and where it is appropriate to use each. The developer needs to be able to debug complex LIVERPS scenarios.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Sublayers | [Layers](./composition-basics/layers.md), [Sublayers](./creating-composition-arcs/sublayers/index.md), [Exercise: Working with Sublayers](./creating-composition-arcs/sublayers/working-with-sublayers.md), [Sublayers FAQ](./creating-composition-arcs/sublayers/sublayers-faq.md) | **Covered** |
| References | [Referencing Basics](./composition-basics/references.md), [References](./creating-composition-arcs/references-payloads/what-are-references.md), [Exercise: Working With References](./creating-composition-arcs/references-payloads/working-with-references.md), [References FAQ](./creating-composition-arcs/references-payloads/references-faq.md) | **Covered** |
| Payloads | [Payloads](./creating-composition-arcs/references-payloads/what-are-payloads.md), [Exercise: Working With Payloads](./creating-composition-arcs/references-payloads/working-with-payloads.md) | **Covered** |
| Variant sets | [Variant Sets Basics](./composition-basics/variant-sets.md), [Variant Sets](./creating-composition-arcs/variant-sets/what-are-variant-sets.md), [Exercise: Working With Variant Sets](./creating-composition-arcs/variant-sets/working-with-variant-sets.md) | **Covered** |
| Inherits and specializes | [Inherits](./creating-composition-arcs/inherits-specializes/what-is-inherits.md), [Specializes](./creating-composition-arcs/inherits-specializes/what-is-specializes.md), and their exercises | **Covered** |
| When to use each arc | [Encapsulation](./creating-composition-arcs/encapsulation/index.md), [Reference/Payload Pattern](./asset-structure/reference-payload-pattern/index.md), the FAQ lessons above | **Covered** |
| Debug complex LIVERPS scenarios | [Composition Arcs and Strength Ordering](./composition-basics/strength-ordering.md), [What Is LIVERPS?](./creating-composition-arcs/strength-ordering/what-is-liverps.md), [Tracing Through LIVERPS](./creating-composition-arcs/strength-ordering/tracing-through-liverps.md), [What Is Prim Composition?](./creating-composition-arcs/prim-composition.md) | **Covered** |
| Specifiers and default prim | [Specifiers](./composition-basics/specifiers.md), [Default Prim](./composition-basics/default-prim.md) | **Covered** |
| Value resolution across arcs | [Value Resolution](./beyond-basics/value-resolution.md) | **Covered** |
| Value clips | No lesson | **Gap** |
| Layer offsets and time scaling | Mentioned in [Spline Animation](./beyond-basics/spline-animation.md), no dedicated lesson | **Gap** |
| Session layer | No lesson | **Gap** |
| List editing semantics | No lesson | **Gap** |
| Edit targets and layer muting | No lesson | **Gap** |
| Relocates | No lesson | **Gap** |

## Data Exchange (15%)

> Create conceptual data mapping documents, custom importers, exports, and scripts for interchange of data with OpenUSD.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Conceptual data mapping documents | [What Is Data Exchange?](./data-exchange/data-exchange/what-is-data-exchange.md), [What Is Data Extraction?](./data-exchange/data-extraction/what-is-data-extraction.md) | **Covered** |
| Custom importers | [Exercise: Anatomy of a Converter](./data-exchange/data-exchange/exercise.md), [Exercise: Extracting Geometry](./data-exchange/data-extraction/exercise-extracting-geometry.md), [Exercise: Extracting Materials](./data-exchange/data-extraction/exercise-extracting-materials.md) | **Covered** |
| Custom exporters | [What Is Data Transformation?](./data-exchange/data-transformation/what-is-data-transformation.md), [Exercise: Adding an Export Option](./data-exchange/data-transformation/exercise-export-option.md), [Exercise: Transforming the Prim Hierarchy](./data-exchange/data-transformation/transformation-hierarchy.md) | **Covered** |
| Validating exchanged data | [What Is Asset Validation?](./data-exchange/asset-validation/what-is-asset-validation.md), [Exercise: Asset Validation and Testing](./data-exchange/asset-validation/exercise-asset-validation-testing.md) | **Covered** |
| USDZ packaging for delivery | Introduced in [OpenUSD File Formats](./stage-setting/usd-file-formats.md); packaging workflow not taught | **Partial** |
| Asset resolution for external references | No lesson | **Gap** |

## Pipeline Development (14%)

> Perform high-level tasks that are important for a well-rounded OpenUSD developer or architect, including designing the pipeline, asset management, versioning, diagramming, documenting, UI/UX, writing a USD exporter hook to transform data into your pipeline's preferred structure, managing build configurations, and flattening and removing proprietary dependencies from an asset.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Designing the pipeline | [Principles of Asset Structure](./asset-structure/asset-structure-principles/index.md), [Workstreams](./asset-structure/workstreams/index.md), [Modeling Workstreams With Layer Stacks](./asset-structure/workstreams/modeling-workstreams.md) | **Covered** |
| Writing a USD exporter hook | [Exercise: Adding an Export Option](./data-exchange/data-transformation/exercise-export-option.md) | **Covered** |
| Asset management | [Model Hierarchy](./asset-structure/model-hierarchy/index.md), [Asset Parameterization](./asset-structure/asset-parameterization/index.md) cover structure, but not asset tracking or dependency management | **Partial** |
| Versioning | No lesson | **Gap** |
| Diagramming and documenting a pipeline | No lesson | **Gap** |
| UI/UX | No lesson | **Gap** |
| Managing build configurations | No lesson | **Gap** |
| Flattening and removing proprietary dependencies | Flattening appears incidentally in [Units in OpenUSD](./beyond-basics/units.md); no lesson teaches it | **Gap** |

## Data Modeling (13%)

> Understand Usd and Sdf data structures and data types, including prims, properties (attributes/relationships), primvars, valueTypes (float, token, matrix4d, etc.), timeSamples, and built-in USD schemas.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Stages and prims | [Stage](./stage-setting/stage.md), [Prims](./stage-setting/prims.md), [Prim and Property Paths](./stage-setting/prim-property-paths.md) | **Covered** |
| Properties: attributes and relationships | [Properties](./stage-setting/properties/index.md), [Attributes](./stage-setting/properties/attributes.md), [Relationships](./stage-setting/properties/relationships.md) | **Covered** |
| Primvars | [Primvars](./beyond-basics/primvars.md), [Exercise: Lofting Primvars](./asset-structure/reference-payload-pattern/lofting-primvars.md) | **Covered** |
| timeSamples | [Time Codes and Time Samples](./stage-setting/timecodes-timesamples.md), [Value Resolution](./beyond-basics/value-resolution.md), [Spline Animation](./beyond-basics/spline-animation.md) | **Covered** |
| Metadata | [Metadata](./stage-setting/metadata.md), [Active and Inactive Prims](./beyond-basics/active-inactive-prims.md) | **Covered** |
| Custom properties | [Custom Properties](./beyond-basics/custom-properties.md) | **Covered** |
| Built-in USD schemas | [Schemas](./scene-description-blueprints/schemas.md), [Scope](./scene-description-blueprints/scope.md), [Xform](./scene-description-blueprints/xform.md), [XformCommonAPI](./scene-description-blueprints/xformcommonapi.md), [Lights](./scene-description-blueprints/lights.md) | **Partial** |
| valueTypes (float, token, matrix4d, etc.) | [Attributes](./stage-setting/properties/attributes.md) explains that attributes are typed, but doesn't survey the type system | **Partial** |
| Sdf data structures (`SdfLayer`, prim specs, property specs) | [OpenUSD Modules](./stage-setting/usd-modules.md) introduces `Sdf`; layer and spec authoring is not taught | **Partial** |
| Stage traversal | [Stage Traversal](./beyond-basics/stage-traversal.md) | **Covered** |
| Collections | No lesson | **Gap** |
| Purpose and visibility | No lesson | **Gap** |

## Debugging and Troubleshooting (11%)

> Introspect USD stages to fix unexpected or undesired composition results, identify poorly authored data, and optimize load and render times.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Introspect stages to fix composition results | [What Is Prim Composition?](./creating-composition-arcs/prim-composition.md), [Tracing Through LIVERPS](./creating-composition-arcs/strength-ordering/tracing-through-liverps.md), [Installing usdview](./usdview-install-instructions.md) | **Covered** |
| Identify poorly authored data | [What Is Asset Validation?](./data-exchange/asset-validation/what-is-asset-validation.md), [Exercise: Asset Validation and Testing](./data-exchange/asset-validation/exercise-asset-validation-testing.md) | **Covered** |
| Optimize load times | [Payloads](./creating-composition-arcs/references-payloads/what-are-payloads.md), [Active and Inactive Prims](./beyond-basics/active-inactive-prims.md), [Asset Modularity and Instancing](./asset-modularity-instancing/index.md) | **Covered** |
| Optimize render times | [Asset Modularity and Instancing](./asset-modularity-instancing/index.md), [Hydra](./beyond-basics/hydra.md) | **Covered** |
| Debug flags (`TF_DEBUG`) | No lesson | **Gap** |
| Profiling with the Trace library | No lesson | **Gap** |
| Composition introspection APIs (`GetPrimStack`, `Pcp` prim indices) | usdview-based inspection only; the Python APIs are not taught | **Partial** |
| Stage population masks | No lesson | **Gap** |

## Content Aggregation (10%)

> Build modular, reusable components; leverage instancing (native and point) to optimize a scene; and apply different strategies for overriding an instanced asset for efficient, optimized, and collaborative aggregation of assets (models) to build large scenes.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Build modular, reusable components | [Asset Modularity](./asset-modularity-instancing/asset-modularity/index.md), [Principles of Asset Structure](./asset-structure/asset-structure-principles/index.md), [Asset Parameterization](./asset-structure/asset-parameterization/index.md) | **Covered** |
| Native (scenegraph) instancing | [What Is Instancing?](./asset-modularity-instancing/what-is-instancing.md), [Authoring Scenegraph Instancing](./asset-modularity-instancing/authoring-scenegraph-instancing/index.md), [Nested Instancing](./asset-modularity-instancing/authoring-scenegraph-instancing/nested-instancing.md) | **Covered** |
| Point instancing | [Authoring Point Instancing](./asset-modularity-instancing/authoring-point-instancing/index.md), [Refining Point Instances](./asset-modularity-instancing/refining-point-instances.md) | **Covered** |
| Strategies for overriding an instanced asset | [Refining Scenegraph Instances](./asset-modularity-instancing/refining-scenegraph-instances/index.md) and its six refinement lessons | **Covered** |
| Aggregating models into large scenes | [Model Hierarchy](./asset-structure/model-hierarchy/index.md), [Exercise: Assemblies](./asset-structure/model-hierarchy/exercise-assemblies.md), [Exercise: Groups](./asset-structure/model-hierarchy/exercise-groups.md) | **Covered** |
| Instancing trade-offs and FAQs | [Instancing FAQ](./asset-modularity-instancing/instancing-faq.md) | **Covered** |

## Visualization (8%)

> Execute tasks related to UsdGeom, UsdShade, and UsdLux USD domains (e.g., meshes, cameras, materials, and lights). These are domains that are used in almost every USD use case, so we would expect a developer to be more familiar with these domains.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| UsdLux: lights | [Lights](./scene-description-blueprints/lights.md) | **Covered** |
| UsdGeom: transforms and hierarchy | [Xform](./scene-description-blueprints/xform.md), [XformCommonAPI](./scene-description-blueprints/xformcommonapi.md), [Scope](./scene-description-blueprints/scope.md) | **Covered** |
| Rendering architecture | [Hydra](./beyond-basics/hydra.md) | **Covered** |
| UsdGeom: meshes and geometry | Meshes appear in [Schemas](./scene-description-blueprints/schemas.md) and data exchange exercises; no lesson covers mesh topology, normals, extents, or subdivision | **Partial** |
| UsdShade: materials and shaders | Reading materials is covered in [Exercise: Extracting Materials](./data-exchange/data-extraction/exercise-extracting-materials.md); no lesson teaches authoring material networks | **Partial** |
| Cameras | No lesson | **Gap** |
| Render settings, products, and vars | No lesson | **Gap** |

## Customizing USD (6%)

> Understand USD plugin development to extend USD's functionality, including the creation of custom schemas, file format plugins, custom model kinds, and variant fallback selections.

| Objective | Learn OpenUSD coverage | Status |
|---|---|---|
| Custom model kinds | [Model Kinds](./beyond-basics/model-kinds.md) notes that custom kinds exist, but doesn't cover registering them | **Partial** |
| USD plugin development | No lesson | **Gap** |
| Creating custom schemas | No lesson | **Gap** |
| File format plugins | No lesson | **Gap** |
| Variant fallback selections | No lesson | **Gap** |

```{seealso}
Customizing USD is the least-covered topic in this curriculum. Study it from [Generating New Schema Classes](https://openusd.org/release/tut_generating_new_schema.html) and the [Plugin Architecture](https://openusd.org/release/api/plug_page_front.html) documentation on openusd.org.
```

## Contributing to Close These Gaps

Every row marked **Gap** or **Partial** is an opportunity to contribute. If you'd like to write one of these lessons, see the [Contributing Guidelines](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/blob/main/CONTRIBUTING.md) or [open an issue](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues/new) to discuss it first.

When you add or remove a lesson, update this page so the map stays accurate.
