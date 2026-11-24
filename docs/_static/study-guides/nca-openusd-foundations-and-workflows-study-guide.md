---
title: "NVIDIA Certified Associate: OpenUSD Foundations and Workflows (NCA-OUSD) study guide"
exam_code: "NCA-OUSD"
version: "0.4"
date: "24 November 2026"
status: "Technical review complete; program decisions outstanding"
edition: "agent-ingestible markdown"
generated_by: "nca/study-guide/build_agent_md.py"
disclaimer: "Instructional material derived from a provisional exam blueprint. Not an approved exam specification, passing standard, or guarantee of readiness. Practice items are formative; they are not operational exam questions."
counts:
  lessons: 30
  supplements: 3
  cases: 5
  questions: 24
  readings: 33
usage_for_agents:
  - "Each lesson, supplement, case and question carries an HTML-comment metadata block."
  - "Filter on domain, task or reading id to scope generated items to a blueprint area."
  - "check/expected pairs are worked answers; use them as answer keys or as seeds for new scenarios."
  - "Do not reproduce practice items verbatim as exam questions; generate fresh scenarios."
domains:
  - id: 1
    title: "OpenUSD fundamentals"
    tasks: ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]
  - id: 2
    title: "Composition and scene assembly"
    tasks: ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7"]
  - id: 3
    title: "Workflow architecture"
    tasks: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8"]
  - id: 4
    title: "OpenUSD value and ecosystem"
    tasks: ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8"]
readings:
  - id: "R01"
    title: "Stage"
    url: "https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html"
    focus: "Composed scene versus source documents."
  - id: "R02"
    title: "Attributes"
    url: "https://docs.nvidia.com/learn-openusd/latest/stage-setting/properties/attributes.html"
    focus: "Typed property values; skip Python details."
  - id: "R03"
    title: "Relationships"
    url: "https://docs.nvidia.com/learn-openusd/latest/stage-setting/properties/relationships.html"
    focus: "Targets connecting scene objects."
  - id: "R04"
    title: "OpenUSD File Formats"
    url: "https://docs.nvidia.com/learn-openusd/latest/stage-setting/usd-file-formats.html"
    focus: "USDA, USDC, USD, and USDZ roles."
  - id: "R05"
    title: "Schemas"
    url: "https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/schemas.html"
    focus: "Typed schemas and API schemas; conceptual distinctions."
  - id: "R06"
    title: "Time Codes and Time Samples"
    url: "https://docs.nvidia.com/learn-openusd/latest/stage-setting/timecodes-timesamples.html"
    focus: "Values over time; separate authored data from simulation behavior."
  - id: "R07"
    title: "Metadata"
    url: "https://docs.nvidia.com/learn-openusd/latest/stage-setting/metadata.html"
    focus: "Non-time-sampled information on layers, prims, and properties."
  - id: "R08"
    title: "Sublayers"
    url: "https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/what-are-sublayers.html"
    focus: "Combining layer contributions at existing scene paths."
  - id: "R09"
    title: "References"
    url: "https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/references-payloads/what-are-references.html"
    focus: "Reusing asset content at a destination prim."
  - id: "R10"
    title: "Payloads"
    url: "https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/references-payloads/what-are-payloads.html"
    focus: "Selective loading of scene content."
  - id: "R11"
    title: "Variant Sets"
    url: "https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/variant-sets/what-are-variant-sets.html"
    focus: "Authored alternatives and their selection."
  - id: "R12"
    title: "What Is LIVERPS?"
    url: "https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/strength-ordering/what-is-liverps.html"
    focus: "Strength ordering; note its explicit LIVRPS/relocates transition notice."
  - id: "R13"
    title: "Value Resolution"
    url: "https://docs.nvidia.com/learn-openusd/latest/beyond-basics/value-resolution.html"
    focus: "Resolving values from composed sources; distinguish defaults and samples."
  - id: "R14"
    title: "Modeling Workstreams With Layer Stacks"
    url: "https://docs.nvidia.com/learn-openusd/latest/asset-structure/workstreams/modeling-workstreams.html"
    focus: "Sparse contributions and ownership; layers are not a version-history system."
  - id: "R15"
    title: "What Is an Asset Interface?"
    url: "https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/asset-interface-pt1.html"
    focus: "Stable public structure for downstream use."
  - id: "R16"
    title: "What Is Data Exchange?"
    url: "https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-exchange/what-is-data-exchange.html"
    focus: "Translation boundaries and information requirements."
  - id: "R17"
    title: "What Is Asset Validation?"
    url: "https://docs.nvidia.com/learn-openusd/latest/data-exchange/asset-validation/what-is-asset-validation.html"
    focus: "Validation concepts; no command memorization required."
  - id: "R18"
    title: "Hydra"
    url: "https://docs.nvidia.com/learn-openusd/latest/beyond-basics/hydra.html"
    focus: "Scene/render separation and renderer integrations."
  - id: "R19"
    title: "What Is Instancing?"
    url: "https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/what-is-instancing.html"
    focus: "Repetition, shared data, and customization tradeoffs."
  - id: "R20"
    title: "Custom Properties"
    url: "https://docs.nvidia.com/learn-openusd/latest/beyond-basics/custom-properties.html"
    focus: "Project-specific data without immediately creating a schema."
  - id: "R21"
    title: "Introduction to USD; Supplemental video (YouTube)"
    url: "https://openusd.org/release/intro.html"
    focus: "Read “Why use USD?”, represent/compose/image sections, and capability limits."
  - id: "R22"
    title: "Alliance for OpenUSD"
    url: "https://aousd.org/"
    focus: "Mission, standardization, and ecosystem collaboration."
  - id: "R23"
    title: "Learn OpenUSD curriculum"
    url: "https://docs.nvidia.com/learn-openusd/latest/index.html"
    focus: "Optional navigation and enrichment; its development-certification scope differs from this guide."
  - id: "R24"
    title: "Encoding Stage Linear Units"
    url: "https://openusd.org/release/api/group___usd_geom_linear_units__group.html"
    focus: "Read the introductory metric and assembly rules; account for transforms rather than assuming automatic geometric conversion."
  - id: "R25"
    title: "Conceptual Data Mapping"
    url: "https://docs.omniverse.nvidia.com/usd/latest/technical_reference/conceptual_data_mapping/index.html"
    focus: "Mapping source concepts, recording transformations and documenting limitations."
  - id: "R26"
    title: "Scenegraph Instancing"
    url: "https://openusd.org/release/api/_usd__page__scenegraph_instancing.html"
    focus: "Shared descendants, editable instance-root properties and limits on descendant edits; skip API exercises."
  - id: "R27"
    title: "USD Physics Schema"
    url: "https://openusd.org/release/api/usd_physics_page_front.html"
    focus: "Representation of rigid bodies, collisions and joints; no simulator implementation required."
  - id: "R28"
    title: "Relationships and restrictions"
    url: "https://openusd.org/release/api/class_usd_relationship.html"
    focus: "Read the class description and Relationship Restrictions section; targets must remain reachable after composition."
  - id: "R29"
    title: "Stage flattening"
    url: "https://openusd.org/release/api/class_usd_stage.html"
    focus: "Read Flatten under Flatten & Export Utilities: selected variant results survive, original variant sets do not."
  - id: "R30"
    title: "Attribute values and interpolation"
    url: "https://openusd.org/release/api/class_usd_attribute.html"
    focus: "Default versus numeric-time queries, held/linear interpolation and value-source conditions."
  - id: "R31"
    title: "OpenUSD schema hierarchy"
    url: "https://openusd.org/release/api/hierarchy.html"
    focus: "Recognize UsdGeom, UsdShade, UsdLux, UsdSkel and UsdPhysics families; no hierarchy memorization required."
  - id: "R32"
    title: "CollisionAPI"
    url: "https://openusd.org/release/api/class_usd_physics_collision_a_p_i.html"
    focus: "Applied collision properties on supported geometric prims; distinguish API schemas from typed schemas."
  - id: "R33"
    title: "USDZ File Format Specification"
    url: "https://openusd.org/release/spec_usdz.html"
    focus: "Package structure and reading constraints; conceptual delivery implications only."
tasks:
  - id: "1.1"
    topic: "Stages, layers, prims, properties"
    readings: ["R01"]
    check: "E1.1"
    practice: ["P01"]
  - id: "1.2"
    topic: "Attributes and relationships"
    readings: ["R02", "R03", "R28"]
    check: "E1.2"
    practice: ["P02", "P20"]
  - id: "1.3"
    topic: "File formats"
    readings: ["R04", "R33"]
    check: "E1.3"
    practice: ["P03"]
  - id: "1.4"
    topic: "Representable domains"
    readings: ["R21", "R27", "R31"]
    check: "E1.4"
    practice: ["P04", "P19"]
  - id: "1.5"
    topic: "Schemas"
    readings: ["R05", "R32"]
    check: "E1.5"
    practice: ["P04", "P19"]
  - id: "1.6"
    topic: "Defaults and time samples"
    readings: ["R06", "R13", "R30"]
    check: "E1.6"
    practice: ["P02", "P22"]
  - id: "1.7"
    topic: "Metadata"
    readings: ["R07"]
    check: "E1.7"
    practice: ["P02"]
  - id: "2.1"
    topic: "Composition mechanisms"
    readings: ["R08", "R11"]
    check: "E2.1"
    practice: ["P06", "P07"]
  - id: "2.2"
    topic: "Strength ordering"
    readings: ["R12"]
    check: "E2.2"
    practice: ["P05"]
  - id: "2.3"
    topic: "Arc selection"
    readings: ["R08", "R11"]
    check: "E2.3"
    practice: ["P06", "P07"]
  - id: "2.4"
    topic: "References and payloads"
    readings: ["R09", "R10"]
    check: "E2.4"
    practice: ["P06"]
  - id: "2.5"
    topic: "Non-destructive collaboration"
    readings: ["R14"]
    check: "E2.5"
    practice: ["P09"]
  - id: "2.6"
    topic: "Variant sets"
    readings: ["R11"]
    check: "E2.6"
    practice: ["P07"]
  - id: "2.7"
    topic: "Missing opinions"
    readings: ["R13"]
    check: "E2.7"
    practice: ["P08"]
  - id: "3.1"
    topic: "Workstreams"
    readings: ["R14"]
    check: "E3.1"
    practice: ["P09"]
  - id: "3.2"
    topic: "Workflow diagrams"
    readings: ["R16"]
    check: "E3.2"
    practice: ["P10"]
  - id: "3.3"
    topic: "Naming conventions"
    readings: ["R15"]
    check: "E3.3"
    practice: ["P11"]
  - id: "3.4"
    topic: "Versioning"
    readings: ["R14", "R15"]
    check: "E3.4"
    practice: ["P10", "P21"]
  - id: "3.5"
    topic: "Extension decisions"
    readings: ["R05", "R20"]
    check: "E3.5"
    practice: ["P04"]
  - id: "3.6"
    topic: "Dependencies and handoffs"
    readings: ["R15", "R16"]
    check: "E3.6"
    practice: ["P11", "P21"]
  - id: "3.7"
    topic: "Asset guidelines"
    readings: ["R15", "R17", "R24"]
    check: "E3.7"
    practice: ["P12", "P17", "P24"]
  - id: "3.8"
    topic: "Workflow bottlenecks"
    readings: ["R10", "R19", "R26"]
    check: "E3.8"
    practice: ["P15", "P23"]
  - id: "4.1"
    topic: "Stakeholder benefits"
    readings: ["R21"]
    check: "E4.1"
    practice: ["P16"]
  - id: "4.2"
    topic: "Hydra architecture"
    readings: ["R18"]
    check: "E4.2"
    practice: ["P13", "P14"]
  - id: "4.3"
    topic: "Visualization strategy"
    readings: ["R18"]
    check: "E4.3"
    practice: ["P13", "P14"]
  - id: "4.4"
    topic: "Tool compatibility"
    readings: ["R16", "R17", "R29"]
    check: "E4.4"
    practice: ["P12", "P14", "P24"]
  - id: "4.5"
    topic: "Interoperability"
    readings: ["R16", "R25"]
    check: "E4.5"
    practice: ["P12", "P18", "P24"]
  - id: "4.6"
    topic: "Scalability"
    readings: ["R10", "R19", "R26"]
    check: "E4.6"
    practice: ["P15", "P23"]
  - id: "4.7"
    topic: "Adoption cases"
    readings: ["R21"]
    check: "E4.7"
    practice: ["P16"]
  - id: "4.8"
    topic: "AOUSD and community"
    readings: ["R22"]
    check: "E4.8"
    practice: ["P14", "P16"]
supplemental_labels:
  - label: "1.8"
    topic: "Schema mapping, units, conceptual mapping and two-phase exchange"
    readings: ["R16", "R24", "R25", "R31"]
    check: "ES1"
    practice: ["P17", "P19"]
  - label: "1.9"
    topic: "Upstream asset revisions and downstream compatibility"
    readings: ["R14", "R15", "R21"]
    check: "ES2"
    practice: ["P21"]
  - label: "2.8"
    topic: "Payload loading, instancing and sparse override decisions"
    readings: ["R08", "R10", "R26"]
    check: "ES3"
    practice: ["P15", "P23"]
questions_index:
  - id: "P01"
    answer: "B"
    tasks: ["1.1"]
    readings: ["R01"]
  - id: "P02"
    answer: "D"
    tasks: ["1.2", "1.6", "1.7"]
    readings: ["R02", "R03", "R06", "R07"]
  - id: "P03"
    answer: "A"
    tasks: ["1.3"]
    readings: ["R04"]
  - id: "P04"
    answer: "C"
    tasks: ["1.4", "1.5", "3.5"]
    readings: ["R05", "R20", "R21"]
  - id: "P05"
    answer: "B"
    tasks: ["2.2"]
    readings: ["R12"]
  - id: "P06"
    answer: "A"
    tasks: ["2.1", "2.3", "2.4"]
    readings: ["R09", "R10"]
  - id: "P07"
    answer: "D"
    tasks: ["2.1", "2.3", "2.6"]
    readings: ["R11"]
  - id: "P08"
    answer: "C"
    tasks: ["2.7"]
    readings: ["R12", "R13"]
  - id: "P09"
    answer: "A"
    tasks: ["2.5", "3.1"]
    readings: ["R14"]
  - id: "P10"
    answer: "C"
    tasks: ["3.2", "3.4"]
    readings: []
  - id: "P11"
    answer: "B"
    tasks: ["3.3", "3.6"]
    readings: ["R15"]
  - id: "P12"
    answer: "D"
    tasks: ["3.7", "4.4", "4.5"]
    readings: ["R16", "R17"]
  - id: "P13"
    answer: "A"
    tasks: ["4.2", "4.3"]
    readings: ["R18"]
  - id: "P14"
    answer: "C"
    tasks: ["4.2", "4.3", "4.4", "4.8"]
    readings: ["R18", "R22"]
  - id: "P15"
    answer: "D"
    tasks: ["3.8", "4.6"]
    readings: ["R10", "R19"]
  - id: "P16"
    answer: "B"
    tasks: ["4.1", "4.7", "4.8"]
    readings: []
  - id: "P17"
    answer: "C"
    tasks: []
    readings: ["R24"]
  - id: "P18"
    answer: "A"
    tasks: ["4.5"]
    readings: ["R16", "R25"]
  - id: "P19"
    answer: "D"
    tasks: ["1.4", "1.5"]
    readings: ["R05", "R27", "R32"]
  - id: "P20"
    answer: "B"
    tasks: ["1.2"]
    readings: ["R03", "R28"]
  - id: "P21"
    answer: "B"
    tasks: ["3.4", "3.6"]
    readings: ["R14", "R15"]
  - id: "P22"
    answer: "C"
    tasks: ["1.6"]
    readings: ["R06", "R13", "R30"]
  - id: "P23"
    answer: "A"
    tasks: ["3.8", "4.6"]
    readings: ["R10", "R19", "R26"]
  - id: "P24"
    answer: "D"
    tasks: ["3.7", "4.4", "4.5"]
    readings: ["R16", "R17"]
---

# NCA-OUSD study guide — agent edition

Version 0.4 · 24 November 2026 · Technical review complete; program decisions outstanding

This file carries the same content as the PDF edition, with per-item metadata for machine consumption. Every lesson has a worked check; every practice question has a single key and a rationale for all four options.

## Domain 1 — OpenUSD fundamentals

### 1.1 Stages, layers, prims, and properties

<!-- item
  type: lesson
  id: 1.1
  domain: 1
  readings: R01
  check: E1.1
  practice: P01
-->

A **stage** is the composed scene an application works with. A **layer** contains authored scene description that may contribute to it. A **prim** is an object at a scene path; a **property** belongs to a prim. Several layers can contribute to one prim, so counting files does not tell you how many objects appear in the scene.

Imagine an exhibit scene with `/Exhibit/Display`: one layer defines the display and another changes its position. The stage presents the composed display. The root layer is the entry point to the composition, not necessarily the location of all its data. Read **R01**.

**Check E1.1:** A reviewer sees a camera whose lens setting comes from a separate review layer. Identify the stage, prim, property, and contributing layer.

**Expected:** The composed review scene is the stage; the camera is a prim; its focal length is an attribute/property; the review layer supplies that setting. The camera need not be fully defined in that layer.

### 1.2 Attributes and relationships

<!-- item
  type: lesson
  id: 1.2
  domain: 1
  readings: R02, R03, R28
  check: E1.2
  practice: P02, P20
-->

An **attribute** holds typed values, such as a number, vector, or array. A **relationship** identifies target scene objects. Think “what is its value?” versus “which object does it refer to?” Relationships may target prims or properties. Follow established schema conventions instead of inventing a relationship merely because two concepts seem associated. Read **R02–R03**.

A relationship's target paths participate in composition. A string containing a path does not automatically supply that behavior. Keep reusable dependencies inside the referenced asset's public structure, or deliberately establish the external connection in the consuming scene. A target outside the referenced subtree may become unreachable; a relationship is not a general-purpose promise that any cross-file dependency will resolve. Read **R28**.

**Check E1.2:** A custom inspection record needs a measured temperature and a link to the inspected component. Which property category fits each?

**Expected:** Use an attribute for the numeric measurement and a relationship for the target component. Document the measurement's units and semantics as part of the data contract.

### 1.3 Choosing file formats

<!-- item
  type: lesson
  id: 1.3
  domain: 1
  readings: R04, R33
  check: E1.3
  practice: P03
-->

**USDA** is readable text, useful for inspection and small illustrative files. **USDC** is a binary representation, useful for production data. **USD** is an extension that can represent either encoding. **USDZ** packages content for supported delivery workflows; it is not merely a smaller spelling of USDC. Format choice does not establish which opinion wins in composition. Read **R04**.

USDZ is an uncompressed package with layout constraints, intended for reading and delivery rather than incremental in-place authoring. Plan to update the working sources and regenerate the package when its contents change. A package format does not replace dependency and consumer checks. Read **R33**.

**Check E1.3:** Choose a format for a short text-review example, a large geometry layer, and a packaged delivery to a consumer that requests USDZ.

**Expected:** USDA, USDC, and USDZ respectively. Confirm recipient support and required dependencies; these choices are based on use, not a universal rule that one format is best.

### 1.4 Represented data versus executing behavior

<!-- item
  type: lesson
  id: 1.4
  domain: 1
  readings: R21, R27, R31
  check: E1.4
  practice: P04, P19
-->

OpenUSD includes schemas for scene domains such as geometry, materials, lights, cameras, skeletal data, and physics descriptions. Recording a description is different from running the system that consumes it. A scene can contain motion samples without containing the original application's editable animation rig. A physics description needs a compatible simulation runtime to produce simulated behavior. Read **R21**, especially its representation and limitation sections.

| Scene information | Standard schema family or type to recognize |
|---|---|
| Polygonal mesh | UsdGeomMesh |
| Materials and shader networks | UsdShadeMaterial and UsdShadeShader |
| Lights | UsdLux schema types |
| Cameras | UsdGeomCamera |
| Skeletons, skinning and skeletal animation | UsdSkel schemas |
| Rigid bodies, collision and joints | UsdPhysics schemas |

These names identify data conventions, not a requirement to write API code. Joint constraints can be represented by joint prims with relationships to bodies; they are not all properties on a mesh. Synchronizing a scene with inventory, orders, or live telemetry requires application logic in addition to scene description. Read **R27**, **R31**.

**Check E1.4:** A partner receives a scene with physics data and expects a viewer to reproduce a simulation. What must be established?

**Expected:** Determine which physics schemas, simulation features, and runtime behavior the receiving application supports. File readability alone does not demonstrate simulation equivalence.

### 1.5 Schemas

<!-- item
  type: lesson
  id: 1.5
  domain: 1
  readings: R05, R32
  check: E1.5
  practice: P04, P19
-->

A **schema** gives data an agreed structure and meaning. A typed schema describes a kind of prim, such as a mesh. An API schema can provide an additional set of properties or behavior conventions to an appropriate prim. A schema is not the same as a file format: changing USDA to USDC does not supply a missing interpretation of specialized data. Read **R05**.

For example, a Mesh can remain a Mesh while CollisionAPI adds collision-related properties. This describes a capability for a compatible physics consumer; applying it does not run a simulator. Distinguish adding a supported API schema from changing the underlying prim type. Read **R32**.

**Check E1.5:** Two tools read a custom sensor prim but disagree about the meaning of its range attribute. Would changing the layer encoding settle the disagreement?

**Expected:** No. The teams need agreed semantics and consumer support, potentially expressed in a shared schema. Encoding alone does not define the sensor model.

### 1.6 Default values and time samples

<!-- item
  type: lesson
  id: 1.6
  domain: 1
  readings: R06, R13, R30
  check: E1.6
  practice: P02, P22
-->

An attribute can have a default value and values authored at time codes. A time sample records a value at a specified point on the scene's time axis; it is not an instruction to run a simulation. Interpretation between samples depends on the value type and interpolation behavior. Separate a query for the default value from a query at a numeric time. Read **R06**; consult **R13** for resolution details.

For an ordinary sampled attribute with no stronger competing value source, a numeric-time query uses the samples, including supported interpolation between them. A default-time query is separate: “default” is not frame zero. For example, one float attribute has default 90, samples 2 at time 0 and 10 at time 8, and linear interpolation. At time 4 it evaluates to 6; a default-time query returns 90. A stronger default can mask weaker samples, so inspect the composed value source before generalizing. Read **R13**, **R30**.

**Check E1.6:** A turntable has rotation samples at times 1 and 25. What additional information would you seek before promising a viewer's result at time 13?

**Expected:** Check interpolation, attribute representation, time settings, and any stronger opinions. Do not infer a physically simulated trajectory from two authored samples.

### 1.7 Metadata

<!-- item
  type: lesson
  id: 1.7
  domain: 1
  readings: R07
  check: E1.7
  practice: P02
-->

**Metadata** describes layers, prims, or properties, subject to the rules of each field. It is not time-sampled. Documentation and custom annotations are examples; metadata can also affect interpretation or composition. “Metadata is just a comment” is therefore an unsafe generalization. Use an appropriate container such as custom data for project annotations rather than assuming arbitrary new metadata fields require no registration. Read **R07**.

For project ownership or review annotations on a prim, use agreed keys in a project-specific portion of its customData dictionary. These annotations do not enforce access controls or approvals. Like other authored information, metadata has composition rules; an annotation can be descriptive even though other metadata fields affect scene behavior.

**Check E1.7:** An asset needs a fixed description and a pressure reading that changes over time. Should both be metadata?

**Expected:** A description can be metadata. Changing pressure belongs in a suitable time-sampled attribute with documented units.

## Domain 2 — Composition and scene assembly

### 2.1 Roles of the main composition mechanisms

<!-- item
  type: lesson
  id: 2.1
  domain: 2
  readings: R08, R11
  check: E2.1
  practice: P06, P07
-->

Choose a mechanism by the relationship you need:

| Need | Useful mechanism |
|---|---|
| Combine contributions already authored at compatible scene paths | Sublayers |
| Bring an asset subtree under a destination prim | Reference |
| Allow included content to be loaded or unloaded selectively | Payload |
| Select among authored alternatives | Variant set |

These mechanisms can be used together. A configuration variant might select content that is payloaded, while an assembly references the asset. Read **R08–R11**.

**Check E2.1:** A display has two manufacturer-authored finish choices and a heavy internal assembly rarely needed in reviews. Name two useful mechanisms.

**Expected:** A variant set for the finish choices and a payload boundary for selectively loaded internals. These meet different requirements.

### 2.2 Composition strength ordering

<!-- item
  type: lesson
  id: 2.2
  domain: 2
  readings: R12
  check: E2.2
  practice: P05
-->

Opinion strength comes from composition structure, not modification timestamps. Within a simple layer stack, the containing layer is stronger than its sublayers, and earlier sublayers are stronger than later ones. Do not extend that simplified example to every nested composition graph without tracing the arcs.

The traditional mnemonic is **LIVRPS**: local, inherits, variants, references, payloads, specializes. Current training introduces **LIVERPS**, which adds relocates between variants and references: local, inherits, variants, relocates, references, payloads, specializes. A relocate remaps a prim path introduced by another arc, so it is stronger than the reference that brought the prim in but weaker than a variant selection. Learn the meaning of strength rather than relying on the acronym alone. The exam's supported version remains a program decision. Read **R12**.

**Check E2.2:** A root layer has no value for a particular attribute. Its first sublayer sets that attribute to 4 and its second sets it to 9. Both are defaults on the same prim, with no other opinions. What resolves?

**Expected:** 4. Re-saving the second file later does not change its relative strength.

### 2.3 Choosing arcs from requirements

<!-- item
  type: lesson
  id: 2.3
  domain: 2
  readings: R08, R11
  check: E2.3
  practice: P06, P07
-->

Translate a requirement into a structural decision. For a traveling exhibition, a published kiosk can be brought into several halls under different prim paths. Meanwhile, accessibility adjustments can be authored against the hall's established paths in a separate contribution layer. The kiosk inclusion and the hall adjustments solve different problems.

Read **R08–R11** and explain the selection, not just the mechanism's name.

**Check E2.3:** One hall needs three separately positioned kiosks, a selectable screen style, and optional internal wiring detail. Describe an assembly.

**Expected:** Reference the kiosk under three placement prims; select its authored style variant for each placement as needed; use its payload arrangement for optional wiring. A sublayer does not itself remap an asset into three placements.

### 2.4 References versus payloads

<!-- item
  type: lesson
  id: 2.4
  domain: 2
  readings: R09, R10
  check: E2.4
  practice: P06
-->

Both support composing content into a scene. A payload adds a deliberate load-control boundary. Selectively unloading detail can help the working set, but the asset must be organized so that information needed without that detail remains accessible. A payload is not a substitute for portable paths or a policy deciding when to load it. Read **R09–R10**.

Payloads are not inherently unloaded: standard stage opening loads them unless an application chooses a different load policy. If an assembly authors an asset root outside its payload, unloading removes that payload's contribution while the externally authored root remains. Replacing payloads with ordinary references removes that load-control choice. A small scene that always needs everything may change little; a large scene with little required detail may pay a substantial extra opening and memory cost. The reference/payload pattern is useful when those requirements exist, not mandatory for every referenced asset.

**Check E2.4:** Reviewers need part identity even when the detailed mesh is unloaded. Where should that identity be authored?

**Expected:** In a lightweight portion of the asset available outside the unloaded payload. Putting required identity only inside that payload defeats the requirement.

### 2.5 Non-destructive collaboration

<!-- item
  type: lesson
  id: 2.5
  domain: 2
  readings: R14
  check: E2.5
  practice: P09
-->

Separate contributions by meaningful ownership. Let a placement team author positioning while another team authors a different, agreed contribution. Changes remain in their respective layers, and composition produces the combined view. This avoids requiring one team to overwrite another team's source, but does not resolve conflicting intentions automatically. Read **R14**.

**Check E2.5:** Two teams both change the same display's position in separate layers. Is the conflict solved because both files are preserved?

**Expected:** No. Composition selects an effective opinion according to strength; the teams must decide which placement is intended. Preserving source work and agreeing on the result are different outcomes.

### 2.6 Variant sets

<!-- item
  type: lesson
  id: 2.6
  domain: 2
  readings: R11
  check: E2.6
  practice: P07
-->

A variant set exposes named alternatives. Selecting one determines which authored alternative contributes. Shared content can stay outside variants; differences can be kept inside them. Variants are not guaranteed to remove duplication if authors put complete copies in every alternative. Read **R11**.

**Check E2.6:** Three signage languages share the same supporting frame. How could the asset avoid maintaining three independent frame copies?

**Expected:** Keep shared frame content common and use alternatives for the language-dependent contribution. Check that the intended variant selection is authored at the right scope.

### 2.7 Why an authored opinion may not appear

<!-- item
  type: lesson
  id: 2.7
  domain: 2
  readings: R13
  check: E2.7
  practice: P08
-->

Start with evidence: identify the exact prim/property path, intended source layer, and expected value. Check whether the layer participates, the relevant content is loaded, the desired variant is selected, and a stronger opinion supplies the result. Confirm the edit target when changes appear in an unexpected source. For animation, inspect the requested time and whether a stronger default masks weaker samples. Read **R13**.

**Check E2.7:** A technician changes a weak layer's default value but the stage still shows a different default from the root layer. What should they investigate before adding another layer?

**Expected:** Inspect the contributing opinions and decide whether the root override is intentional. Correct or remove it only through the owning workflow; adding layers blindly obscures the cause.

## Domain 3 — Workflow architecture

### 3.1 Workstreams with sublayers

<!-- item
  type: lesson
  id: 3.1
  domain: 3
  readings: R14
  check: E3.1
  practice: P09
-->

Start with a responsibility map: team, authored paths/properties, input dependencies, and publication output. Then organize layers around those responsibilities. Avoid using one new sublayer for every historical edit; that confuses workstream organization with version history. Read **R14** and case 1.

**Check E3.1:** Design a boundary between exhibit layout and safety annotation work.

**Expected:** Layout owns placement opinions; safety owns agreed annotations and target relationships. Both use stable scene paths. Document how safety findings trigger a new layout publication without giving the safety layer accidental placement overrides.

### 3.2 Workflow diagrams

<!-- item
  type: lesson
  id: 3.2
  domain: 3
  readings: R16
  check: E3.2
  practice: P10
-->

A useful diagram identifies producers, artifacts, consumers, and checks. Label arrows with what moves: source model, published layer, texture dependencies, validation report, or approval record. Distinguish the flow of files from composition relationships. A box labeled “USD” does not explain who exports, who reviews, or which data survives. Read **R16** and case 2.

Make ownership visible at each publication boundary: name the team responsible for the layer, what it may author, where authoritative changes originate, and who accepts its output. File storage location alone does not answer those questions. A data-flow arrow and a responsibility label describe different parts of the same workflow.

**Check E3.2:** Draw four steps from a source design to an approved visualization, with validation and revision feedback.

**Expected:** Show source authoring → conversion/publication candidate → validation in target consumers → review/approval. Route failures back to the responsible author or converter owner; identify a versioned approved output.

### 3.3 Naming conventions

<!-- item
  type: lesson
  id: 3.3
  domain: 3
  readings: R15
  check: E3.3
  practice: P11
-->

Treat public prim paths as part of an asset's interface. A readable naming convention should distinguish asset identity, scene placement, and release identifier. Renaming a file and changing a prim path are different changes, with different downstream effects. Read **R15** and case 2.

**Check E3.3:** A label used by reviewers changes from “station” to “pod.” Should an established public prim path be renamed immediately?

**Expected:** Evaluate dependent overrides and relationships first. A display label change may satisfy the communication need without changing structural identity; a structural rename requires migration and validation.

### 3.4 Versioning

<!-- item
  type: lesson
  id: 3.4
  domain: 3
  readings: R14, R15
  check: E3.4
  practice: P10, P21
-->

For a reproducible delivery, record which asset revisions and dependencies produced it. An immutable published revision is one useful policy; controlled update channels can serve ongoing work. Separate “latest approved” convenience from “reopen the exact reviewed scene” requirements. Layers do not supply the full policy. Read **R14**, **R15**, and case 2.

**Check E3.4:** An exhibit review must be reproducible after a supplier updates a component. What should its handoff record contain?

**Expected:** The assembly revision, dependency revisions or equivalent fixed resolution context, relevant settings, and review evidence. A floating filename alone does not establish reproducibility.

### 3.5 Custom properties or custom schemas

<!-- item
  type: lesson
  id: 3.5
  domain: 3
  readings: R05, R20
  check: E3.5
  practice: P04
-->

Investigate existing schemas before inventing an extension. A small project-specific field may be represented as a documented custom property. Repeated shared concepts with agreed types, discoverability, and multiple consumers may justify a schema. Creating a schema also creates a maintenance and integration responsibility; it does not make every application understand the data. Read **R05**, **R20**.

**Check E3.5:** A single reporting tool needs an inspection ticket string. Is a new typed prim schema necessarily required?

**Expected:** No. Consider a namespaced custom attribute and a documented contract first. Escalate to schema design when shared semantics and tooling requirements justify it.

### 3.6 Dependencies and handoffs

<!-- item
  type: lesson
  id: 3.6
  domain: 3
  readings: R16
  check: E3.6
  practice: P11, P21
-->

Identify what each downstream task actually depends on. Material work may begin before all geometry is final, yet topology-sensitive work can still be invalidated by changes. Dependency mapping makes those conditions explicit. Include textures, external assets, versions, and application assumptions in the handoff. Read **R16** and case 3.

**Check E3.6:** A supplier updates mesh topology after a surface-related approval. What should happen downstream?

**Expected:** Identify affected consumers and rerun the relevant checks. Parallel authoring does not guarantee that an earlier approval remains valid after its inputs change.

### 3.7 Asset guidelines

<!-- item
  type: lesson
  id: 3.7
  domain: 3
  readings: R15, R17
  check: E3.7
  practice: P12, P17, P24
-->

Write a contract a publisher and consumer can both verify. Specify intended units and axis conventions, public root/path structure, supported schemas, required dependencies, configuration choices, and release identification. Describe acceptable variation as well as failure conditions. Automated validation is useful, but consumer-specific behavior still needs representative checks. Read **R15**, **R17**, and case 3.

**Check E3.7:** A package opens but its textures are missing on another workstation. What guideline and check were likely missing?

**Expected:** A dependency-resolution requirement and a clean-environment handoff check. Successful opening on the author's machine is insufficient evidence of portability.

### 3.8 Match features to bottlenecks

<!-- item
  type: lesson
  id: 3.8
  domain: 3
  readings: R10, R19
  check: E3.8
  practice: P15, P23
-->

State the observed cost before suggesting a feature. Unneeded loaded detail suggests a loading strategy; repeated similar content suggests investigating instancing; accidental source overwrites suggest ownership and layering changes. None of these automatically fixes a slow approval queue. Read **R10**, **R19**, and case 3.

**Check E3.8:** A review scene opens quickly, but sign-off takes a week because nobody owns approval. Would changing references to payloads address the measured delay?

**Expected:** No. Assign review responsibility and turnaround expectations. Use scene-loading changes only for a demonstrated loading problem.

## Domain 4 — OpenUSD value and ecosystem

### 4.1 Explain benefits to stakeholders

<!-- item
  type: lesson
  id: 4.1
  domain: 4
  readings: R21
  check: E4.1
  practice: P16
-->

Connect a capability to an observable outcome: preserving separate contributions may reduce rework; a shared scene representation may reduce repeated translation effort. Explain the assumptions and the remaining integration work. Adoption is a proposal to test, not proof that delivery becomes faster. Read **R21** and case 4.

**Check E4.1:** Rewrite “USD will solve our collaboration problems” as a testable pilot claim.

**Expected:** For example: “Separate layout and annotation publications, then measure overwritten work and review turnaround across two iterations.” State who owns the trial and what would count as improvement.

### 4.2 Hydra and renderer integration

<!-- item
  type: lesson
  id: 4.2
  domain: 4
  readings: R18
  check: E4.2
  practice: P13, P14
-->

Hydra separates scene-facing integration from renderer-specific work. A render delegate implements a renderer's side of that integration. This creates a reusable architectural boundary; it does not edit the stage's layer stack on behalf of the author. Read **R18**. The delegate model is a conceptual introduction; newer Hydra material also discusses scene indices, and implementation details are outside this guide.

**Check E4.2:** A viewer team wants a second rendering backend. What boundary should they evaluate, and what still needs testing?

**Expected:** Evaluate the backend's Hydra integration, then test required scene features, materials, settings, and application compatibility.

### 4.3 Interactive and offline visualization

<!-- item
  type: lesson
  id: 4.3
  domain: 4
  readings: R18
  check: E4.3
  practice: P13, P14
-->

Hydra can support interactive viewing and final rendering through suitable integrations. A shared rendering setup can make reviews easier to compare, but renderer, camera, lighting, color management, and scene state matter. Architectural compatibility does not promise image equality. Read **R18** and case 4.

**Check E4.3:** Two tools show different brightness for the same scene. What would you align before declaring the asset inconsistent?

**Expected:** Compare render delegate, relevant renderer settings, exposure/color management, camera, lighting, and scene state. Sharing the same input filename is not a complete rendering contract.

### 4.4 Evaluate tool compatibility

<!-- item
  type: lesson
  id: 4.4
  domain: 4
  readings: R16, R17, R29
  check: E4.4
  practice: P12, P14, P24
-->

Replace “supports USD” with a feature-based acceptance plan. Check the required import/export direction, composition preservation, geometry, materials, animation, custom data, and versions. Opening a file is one observation, not the entire compatibility decision. Read **R16–R17** and case 3.

Stage flattening keeps the composed result of selected variants and removes their original selection structure. The output can still receive later edits or overrides, but it no longer exposes those original alternatives for selection. Distinguish this from merely combining a layer stack. Also check that tools preserve authored properties they do not interpret when those properties are needed by another consumer; successful rendering does not test that preservation. Read **R29**.

**Check E4.4:** Tool A displays a selected configuration correctly but exports only that flattened result. Is it suitable for a handoff that requires editable alternatives?

**Expected:** Not on that evidence. Test preservation of the alternatives and composition required downstream, or explicitly redesign the handoff around a baked deliverable.

### 4.5 Interoperability opportunities

<!-- item
  type: lesson
  id: 4.5
  domain: 4
  readings: R16, R25
  check: E4.5
  practice: P12, P18, P24
-->

A shared representation can replace some pair-specific exchanges, but source extraction and consumer interpretation remain work. Identify the data that needs to survive each boundary. Geometry may transfer while application-specific procedures require baking, conversion, extensions, or a separate artifact. Read **R16**.

A conceptual mapping describes which source concepts correspond to which USD concepts, plus units, transformations and known losses. NVIDIA's two-phase exchange approach first extracts into USD with source fidelity in mind, then applies optional transformations for particular consumers. It is a useful pipeline design, not a universal requirement that every tool perform two exports. See supplement S1 and **R25**.

**Check E4.5:** A consumer only needs final geometry and material assignments, while another needs editable source procedures. Should the same export acceptance criteria apply?

**Expected:** No. Define criteria per consumer. A successful visualization exchange need not be a successful editable round trip.

### 4.6 Large-scene scalability

<!-- item
  type: lesson
  id: 4.6
  domain: 4
  readings: R10, R19, R26
  check: E4.6
  practice: P15, P23
-->

Payloads control which content is loaded. Instancing can share repeated structure where per-copy editing requirements allow it. They address different costs and can coexist. Measure memory, load time, and interaction for a representative scene rather than promising a fixed performance gain. Read **R10**, **R19**.

With scenegraph instancing, compatible instances share descendant structure, while each instance root can retain its own placement transform. Arbitrary per-instance edits beneath that root are restricted; choose a suitable variant/refinement strategy or deinstance the exceptions. Sharing usually matters more as repetition and subtree size grow. Neither a reference nor a payload alone guarantees this scenegraph sharing. Read **R26** and supplement S3.

**Check E4.6:** An installation has thousands of identical fixtures, each positioned differently, and rarely viewed service interiors. Suggest two investigations.

**Expected:** Investigate instancing for repeated fixture structure and payloads for optional detail. Confirm that necessary per-instance edits and unloaded metadata still work.

### 4.7 Adoption cases and organizational goals

<!-- item
  type: lesson
  id: 4.7
  domain: 4
  readings: R21
  check: E4.7
  practice: P16
-->

A credible adoption case records the current pain, proposed intervention, expected result, cost, and acceptance evidence. Separate technical benefits from staffing, ownership, procurement, and approval decisions. Include a fallback if the pilot cannot preserve required information. Read **R21** and case 4.

Measure the boundary named in the proposal: elapsed handoff time, failed transfers or avoidable rework under comparable conditions. Counts of exported files, trained staff or converted assets measure activity; they are not direct evidence that the target delay improved. Record integration and maintenance effort alongside the outcome.

**Check E4.7:** What evidence would support expanding a pilot beyond a successful demonstration?

**Expected:** Repeatable results on representative assets, measured workflow improvement, documented exceptions, ownership of integrations, and an agreed operating cost. One attractive render is not a complete adoption case.

### 4.8 AOUSD and the community

<!-- item
  type: lesson
  id: 4.8
  domain: 4
  readings: R22
  check: E4.8
  practice: P14, P16
-->

AOUSD provides a forum for interoperability and standardization work. The open-source project, documentation, and community support implementation and learning. These activities do not replace a project's acceptance tests or vendor support agreement. Read **R22**.

**Check E4.8:** A procurement note treats participation in an industry alliance as proof that two products exchange every required feature. What evidence is still needed?

**Expected:** Product/version-specific tests against the workflow's feature requirements. Ecosystem participation and proven compatibility are different kinds of evidence.

## Supplemental topics from the v5 review

### S1 Conceptual mapping, units and exchange stages

<!-- item
  type: supplement
  id: S1
  domain: S
  readings: R16, R24, R25
  check: ES1
  practice: -
-->

Start with the information a consumer needs. Record the source concept, a USD representation, any transformation, and the information that will be lost or remain outside USD. Schema names help express the target representation; they do not demonstrate that a converter preserves it. Read **R25** and lesson 1.4.

| Source requirement | Mapping decision to document |
|---|---|
| Visible surface and assignment | Geometry, shading representation and material bindings |
| An application's procedural controller | Supported scene data or baked output; what editability is lost |
| Numeric lengths | Source units, target units and where conversion occurs |
| Live operational status | Stored scene representation plus the external synchronization owner |

The two-phase design in **R16** separates extraction into USD from optional consumer-specific transformation. An extracted representation might feed both a review application and a lower-detail delivery. Keep their acceptance criteria distinct instead of assuming every consumer needs the same representation.

**Linear-unit reasoning:** metersPerUnit is stage-wide metadata, not an automatic conversion of every referenced asset. With identity transforms and no assembler correction, a part authored 200 units long in centimeters will still span 200 numeric units in a meter-based scene. That would be 200 meters rather than its intended 2 meters. A 0.01 scale correction at the appropriate boundary restores the intended length. Account for existing transforms before applying another correction. Read **R24**.

Check up-axis and animation timing conventions as well as linear units; they are separate parts of a handoff contract. Changing a metadata label without adjusting data or transforms can misdescribe the scene rather than convert it.

**Check ES1:** A supplier delivers a shelf 120 units wide with metersPerUnit 0.01. A meter-based review scene references it with identity transforms and no correction. What width will the review interpret, and what correction meets the intended size?

**Expected:** It spans 120 meters in that scene, rather than the intended 1.2 meters. A 0.01 scale correction, or an equivalent validated conversion, restores the width. Record where conversion occurs so it is not applied twice.

### S2 Updating upstream assets without losing downstream work

<!-- item
  type: supplement
  id: S2
  domain: S
  readings: R14, R15, R21, R31
  check: ES2
  practice: -
-->

Treat an upstream revision as a change to a dependency contract. Identify affected geometry, public paths, relationships, bindings, configuration choices and time-varying data. Compose the chosen revision under the existing downstream contributions where that structure remains appropriate. Stronger layers retain opinions, but a retained opinion is not necessarily meaningful after its target changes. Read **R14–R15** and lessons 3.4–3.6.

For a character update, preserving compatible skeleton/joint identities and public paths may reduce disruption. Substantial topology or rig changes can still require reskinning, rebinding or new animation work in the authoring application. USD's skeletal representation is not a promise to preserve a DCC application's procedural controls. This is a dependency-planning exercise; rig construction is outside this guide's scope. Read **R21**, **R31**.

Compare a representative downstream scene before and after the revision. Check whether overrides still land, relationships still target the intended objects, and required deformation or motion still behaves correctly. Publish the new dependency set only when the handoff criteria are met. Preserve a way to reproduce the earlier approved set.

**Check ES2:** A supplier keeps a display's public path but changes its panel layout and material-binding structure. Does the stable path alone establish that a downstream finish override remains correct?

**Expected:** No. Validate both path resolution and meaning: which panel is targeted, which binding wins, and whether the consumer still gets the intended finish. Update affected downstream opinions through their owner while preserving reproducible revisions.

### S3 Scaling the working set and retaining sparse edits

<!-- item
  type: supplement
  id: S3
  domain: S
  readings: R08, R10, R26
  check: ES3
  practice: -
-->

Separate three questions: what must be loaded, which composed subtrees can be shared, and where the new opinions belong. Payloads, scenegraph instancing and sparse contribution layers answer those different questions. Read **R08**, **R10**, **R26**.

| Requirement | Mechanism and condition |
|---|---|
| Open with optional detail absent | Payload boundaries plus an explicit load policy |
| Repeat compatible internal structure | Instanceable roots, with permitted per-instance placement |
| Apply a small scene-specific revision | Sparse opinions at the intended paths in a suitably strong layer |

For a simple stack, an override sublayer can precede weaker contribution layers; opinions authored directly in the containing layer remain stronger. Adding a layer does not guarantee unchanged performance, and putting it first is not a substitute for checking the full composition context. Compare opening time, memory and the editing operations that matter on representative small and large scenes.

**Check ES3:** A campus scene repeats the same shelter many times, needs a unique placement for each, and rarely needs internal cable detail. Later, one shelter needs a unique internal bracket. Describe a plan and the exception.

**Expected:** Evaluate scenegraph instancing for compatible shelter interiors and payloads with selective loading for cable detail. Keep placements on instance roots. Use a supported refinement strategy or deinstance the bracket exception, then measure the resulting scene; do not promise unrestricted edits inside shared descendants.

### case1 Exhibit collaboration

<!-- item
  type: case
  id: case1
  domain: -
  readings: -
  check: -
  practice: -
-->

**Brief:** A layout team positions installations; a lighting team develops illumination; accessibility specialists annotate reach clearances. They need independent publication and a shared review scene. They do not need simultaneous writes to the same file.

**Proposed design:** Give each workstream a contribution layer. Document shared paths and ownership. Assemble them under a review root, with approved asset publications brought in through references. Establish the intended strength order explicitly. An annotation should target the intended installation rather than carry a redundant copy of its geometry.

**Review:** A lighting export unexpectedly authors installation transforms. Diagnose the unwanted opinions and fix the publishing boundary. Reordering the whole stack might conceal one symptom while changing other intended results.

**Lesson:** Layering preserves separable contributions. Collaboration also requires a contract about what each contribution may change. Related tasks: 2.5, 2.7, 3.1.

### case2 Reproducible supplier delivery

<!-- item
  type: case
  id: case2
  domain: -
  readings: -
  check: -
  practice: -
-->

**Brief:** A supplier updates a display assembly monthly, while a museum must reopen exactly what was approved for an installation.

```text
Supplier source
    |
    | export candidate + dependencies + revision record
    v
Validation in required consumers ----failure----> Supplier/converter owner
    |
    | accepted candidate
    v
Museum review ----requested change----> New candidate revision
    |
    | approval record tied to candidate
    v
Fixed published assembly and dependency set
```

**Proposed design:** Preserve approved revisions and record their dependency resolution. Working scenes may follow an update channel, but installation deliveries identify a fixed set. Keep public prim paths stable where practical; assess dependent overrides before structural changes.

**Review:** Reopen the delivery in its documented environment after the supplier publishes the next revision. Verify that the approved scene remains reproducible and that an intentional upgrade is a separate action.

**Lesson:** Versioning and approval policies surround composition; a layer stack alone is not the approval record. Related tasks: 3.2–3.4, 3.6.

### case3 Consumer-specific handoff

<!-- item
  type: case
  id: case3
  domain: -
  readings: -
  check: -
  practice: -
-->

**Brief:** A design team supplies both a visualization tool and a maintenance-planning tool. Visualization needs material assignments and animation; planning needs part identity and inspection relationships.

**Proposed acceptance contract:** Document public paths, units, revisions, dependencies, and which consumer requires each field. Build a small representative test asset containing those features, including one optional detailed component.

| Check | Evidence to retain |
|---|---|
| Both consumers resolve external dependencies | Open/load report from a clean consumer environment |
| Part identities and inspection targets survive | Inspection of required values and relationship targets |
| Visualization retains required motion and appearance | Time-specific review captures with recorded settings |
| Optional detail can be unloaded without losing required identity | Comparison of loaded and unloaded states |
| A revised asset preserves the promised public interface | Consumer regression review after a controlled update |

**Review:** Distinguish a format-valid asset from a workflow-acceptable asset. If the planner drops a custom relationship, either fix that integration or agree a different information channel; a successful render does not close the issue.

**Lesson:** Compatibility is demonstrated for specified features and directions of travel. Related tasks: 3.5–3.8, 4.4–4.6.

### case4 A measured adoption proposal

<!-- item
  type: case
  id: case4
  domain: -
  readings: -
  check: -
  practice: -
-->

**Brief:** A program manager wants shorter review cycles and freedom to evaluate another renderer. The present process frequently uses mismatched asset revisions and undocumented viewer settings.

**Proposed pilot:** Use a fixed review package and documented rendering conditions. Evaluate two renderer integrations against the features the reviewers need. Track preparation time, revision mismatches, rendering discrepancies requiring investigation, and integration effort.

**Decision:** Expand only if the results meet agreed goals at an acceptable maintenance cost. Keep renderer-specific exceptions explicit. Assign approval ownership separately; the renderer interface does not decide who signs off a model.

**Lesson:** A technical architecture can support an organizational goal, but its benefit depends on the complete operating workflow. Related tasks: 4.1–4.3, 4.7–4.8.

### case5 A revised asset entering a large review scene

<!-- item
  type: case
  id: case5
  domain: -
  readings: -
  check: -
  practice: -
-->

**Brief:** An exhibition library supplies repeated display stands. A revised stand changes an internal mounting plate. The library authors in centimeters; the review scene uses meters and needs only exterior geometry during layout. Approved annotations must remain usable after the update.

**Proposed design:** Record the revision and ownership boundary. Validate an explicit unit conversion once, preserve the promised public interface, and test annotations against the changed internal structure. Keep optional detail behind a payload and define the layout application's load policy. Evaluate instancing for repeated compatible stands; use a supported exception strategy for unique interiors. Related lessons: 1.2, 2.4, 3.4, 3.6, 4.6, S1–S3.

| Acceptance evidence | What it demonstrates |
|---|---|
| Known dimension in the assembled scene | The intended physical scale survives the handoff |
| Annotation target and binding inspection | Existing downstream opinions still mean what reviewers expect |
| Loaded/unloaded comparison | Required exterior and identity remain available |
| Opening time and memory measurements | The chosen structure addresses the observed scene cost |
| Reopening the earlier approved revision set | The update did not remove reproducibility |

**Review:** A visually plausible scene can still have incorrect physical scale or stale annotation targets. Inspect these separately and return failures to the responsible owner. One stronger layer cannot automatically repair unit conventions, dependency compatibility and performance at once.

## Practice questions

Formative items with per-option rationales. Use them to validate understanding or as seeds; do not reuse them verbatim as exam items.

### P01 — Finding the source of a value

<!-- item
  type: question
  id: P01
  answer: B
  tasks: 1.1
  readings: R01
-->

A visitor-center scene contains a camera. An inspection shows that its focal length is authored in a review layer, while its transform comes from a layout layer. What best describes the camera the application reads?

- **A.** A separate camera for each layer contributing a property.
- **B.** A composed prim with properties contributed by different layers.
- **C.** A copy of the camera from whichever file was saved most recently.
- **D.** A camera stored entirely in the stage's root layer.

**Answer: B**

- **A:** Contributing layers need not create separate prims when their opinions address the same composed path.
- **B:** Correct. The prim's properties can come from different contributing sources.
- **C:** File timestamps do not determine composition strength.
- **D:** The root is not required to contain every authored camera property.

*Review: task 1.1; R01.*

### P02 — An inspection measurement

<!-- item
  type: question
  id: P02
  answer: D
  tasks: 1.2, 1.6, 1.7
  readings: R02, R03, R06, R07
-->

A pipeline adds project-specific inspection data to a component. It needs a numeric reading at multiple times and a target identifying the inspected part. Which design best matches those requirements?

- **A.** Put both the reading and the part path in a fixed documentation string.
- **B.** Use a relationship for the reading and a numeric attribute for the part path.
- **C.** Use a separate variant for each reading and store the part as a layer filename.
- **D.** Use a time-sampled attribute for the reading and a relationship for the target.

**Answer: D**

- **A:** A fixed string does not meet the structured time-varying measurement requirement.
- **B:** This reverses the roles of numeric values and scene targets.
- **C:** Configuration selection is not the intended representation for the measurement history.
- **D:** Correct. It separates a sampled value from a target relationship.

*Review: tasks 1.2, 1.6, 1.7; R02, R03, R06, R07.*

### P03 — Text inspection

<!-- item
  type: question
  id: P03
  answer: A
  tasks: 1.3
  readings: R04
-->

A trainer needs a small scene example that learners can inspect in a text editor without converting it first. Which format best meets that need?

- **A.** USDA.
- **B.** USDC.
- **C.** USDZ.
- **D.** USD, with its underlying encoding unspecified.

**Answer: A**

- **A:** Correct. USDA directly supports the stated text-inspection task.
- **B:** USDC is binary and does not meet the no-conversion requirement.
- **C:** A package is not the requested directly readable scene-text example.
- **D:** An unspecified USD encoding does not establish that the file is text.

*Review: task 1.3; R04.*

### P04 — A shared extension

<!-- item
  type: question
  id: P04
  answer: C
  tasks: 1.4, 1.5, 3.5
  readings: R05, R20, R21
-->

Two applications must interpret a supplier-defined component type. Both can open the layer, but they disagree about the meaning of a specialized property. What should the integration team address first?

- **A.** Use a more compact binary encoding for the layer.
- **B.** Move the property into the strongest scene layer.
- **C.** Agree on the property's semantics and verify consumer support.
- **D.** Store the same layer in a delivery package.

**Answer: C**

- **A:** Encoding does not resolve disagreement over meaning.
- **B:** Strength may change which value wins, not its shared interpretation.
- **C:** Correct. The teams need a common semantic contract and compatible implementations.
- **D:** Packaging does not supply the missing semantics.

*Review: tasks 1.4, 1.5, 3.5; R05, R20, R21.*

### P05 — Predicting a default

<!-- item
  type: question
  id: P05
  answer: B
  tasks: 2.2
  readings: R12
-->

A root layer has two sublayers, North followed by South. North authors a default value of 12 for an attribute; South authors 18 for that same attribute at the same prim path. There are no other relevant opinions. What happens when South is saved again without changing the layer order?

- **A.** The result becomes 18 because South has the newer timestamp.
- **B.** The result remains 12 because the order still makes North stronger.
- **C.** The result becomes 15 because the two defaults are averaged.
- **D.** The result disappears until one contribution is removed.

**Answer: B**

- **A:** Recency is not the selection rule here.
- **B:** Correct. Under the stated simple stack, the earlier sublayer remains stronger.
- **C:** These competing defaults are not averaged.
- **D:** Conflicting authored defaults do not by themselves require removing a layer to obtain a result.

*Review: task 2.2; R12.*

### P06 — Unloaded detail

<!-- item
  type: question
  id: P06
  answer: A
  tasks: 2.1, 2.3, 2.4
  readings: R09, R10
-->

A maintenance browser must show equipment identifiers while detailed geometry is unloaded. A supplier has placed both the identifier and geometry inside the same payloaded subtree. Which revision best meets the requirement?

- **A.** Make the identifier available in the lightweight asset interface outside the payload.
- **B.** Store the payload layer using a text encoding.
- **C.** Add another identifier inside the same payloaded subtree.
- **D.** Change the payload file's modification time before delivery.

**Answer: A**

- **A:** Correct. Required identity must remain available when detail is unloaded.
- **B:** Changing encoding does not move the load boundary.
- **C:** Both copies would still be inside the unavailable content.
- **D:** Timestamps do not change what unloading excludes.

*Review: tasks 2.1, 2.3, 2.4; R09, R10.*

### P07 — Authored alternatives

<!-- item
  type: question
  id: P07
  answer: D
  tasks: 2.1, 2.3, 2.6
  readings: R11
-->

A display asset has one shared support structure and two authored screen layouts. Consumers need to choose a layout without maintaining separate complete assets. Which structure best fits?

- **A.** Put both screen layouts at the same paths in equally intended workstream layers.
- **B.** Export a full independent asset whenever a consumer changes its selection.
- **C.** Put the screen-layout choice only in a documentation string.
- **D.** Keep the support common and expose the screen layouts through a variant set.

**Answer: D**

- **A:** Competing contributions do not express the intended named choice clearly.
- **B:** Full independent copies introduce the maintenance burden the requirement seeks to avoid.
- **C:** A descriptive string alone does not select authored composition alternatives.
- **D:** Correct. Common content and variant-specific differences meet the two requirements.

*Review: tasks 2.1, 2.3, 2.6; R11.*

### P08 — A hidden contribution

<!-- item
  type: question
  id: P08
  answer: C
  tasks: 2.7
  readings: R12, R13
-->

A technician changes a default setting in a department layer. Inspection confirms the layer participates, the property path is correct, and a root-layer default still supplies the displayed value. What is the most useful next step?

- **A.** Re-export the department layer with a different file extension.
- **B.** Add another copy of the department layer to the stack.
- **C.** Determine whether the root override is intended and coordinate its correction if needed.
- **D.** Update the department file timestamp to make the edit stronger.

**Answer: C**

- **A:** Encoding does not address the identified stronger opinion.
- **B:** Duplicating a contribution does not explain or resolve ownership of the root override.
- **C:** Correct. The cause is known; the next decision is whether that override is intended.
- **D:** Modification time does not change composition strength.

*Review: task 2.7; R12, R13.*

### P09 — Defining workstream boundaries

<!-- item
  type: question
  id: P09
  answer: A
  tasks: 2.5, 3.1
  readings: R14
-->

An annotation team publishes inspection targets, but its exporter also writes unchanged placement values. Those values sometimes mask later layout updates. What should the team change?

- **A.** Restrict publication to the annotation team's intended contributions.
- **B.** Archive a flattened copy after every annotation edit.
- **C.** Place all annotation layers first regardless of the intended ownership.
- **D.** Add a new layer for every placement value the exporter writes.

**Answer: A**

- **A:** Correct. Sparse publication aligned with ownership removes unintended placement opinions.
- **B:** Archiving may preserve history but does not correct the exporter behavior.
- **C:** Giving annotations blanket strength could preserve the masking problem.
- **D:** More layers do not establish the correct responsibility boundary.

*Review: tasks 2.5, 3.1; R14 and case 1.*

### P10 — Reopening an approval

<!-- item
  type: question
  id: P10
  answer: C
  tasks: 3.2, 3.4
  readings: -
-->

A reviewed assembly depends on an asset alias that resolves to the latest supplier publication. The reviewer must reopen the exact approved result six months later. What should the delivery policy establish?

- **A.** A rule that every supplier publication uses the same filename.
- **B.** A record of the reviewer workstation's screen resolution.
- **C.** A fixed assembly and dependency revision set, or equivalent reproducible resolution context.
- **D.** A stronger review layer without recording which assets it composes.

**Answer: C**

- **A:** A stable filename can still refer to changing content.
- **B:** Screen resolution does not identify the composed dependencies.
- **C:** Correct. Reproducibility requires identifying the actual inputs or an equivalent fixed context.
- **D:** Strength does not establish which upstream revision was used.

*Review: tasks 3.2, 3.4; case 2. This is a workflow-policy recommendation.*

### P11 — Public path changes

<!-- item
  type: question
  id: P11
  answer: B
  tasks: 3.3, 3.6
  readings: R15
-->

A supplier plans to rename a public prim path referenced by downstream overrides. The change is cosmetic from the supplier's perspective. What should happen before release?

- **A.** Assume the overrides will follow because the geometry is unchanged.
- **B.** Identify dependents and validate a migration or preserve the public path.
- **C.** Re-encode the asset in USDC so consumers can infer the renamed prim.
- **D.** Ask consumers to open the scene at a different time code.

**Answer: B**

- **A:** Unchanged geometry does not establish that path-based dependencies follow a rename.
- **B:** Correct. The public structure is part of the downstream contract.
- **C:** Binary encoding does not implement a namespace migration.
- **D:** A time-code change does not repair a structural dependency.

*Review: tasks 3.3, 3.6; R15 and case 2.*

### P12 — A complete handoff

<!-- item
  type: question
  id: P12
  answer: D
  tasks: 3.7, 4.4, 4.5
  readings: R16, R17
-->

A converted scene renders correctly on its author's machine but loses inspection links in the maintenance tool. Both appearance and inspection links are delivery requirements. What is the appropriate acceptance decision?

- **A.** Accept because a rendered image confirms the asset's usability.
- **B.** Accept if the file can also be opened by a second viewer.
- **C.** Accept if the conversion produced no syntax errors.
- **D.** Hold acceptance until required links are preserved or an agreed alternative meets the requirement.

**Answer: D**

- **A:** Visual appearance does not demonstrate preservation of inspection data.
- **B:** Another viewer's successful open does not test the missing links.
- **C:** Syntactic validity does not establish workflow acceptance.
- **D:** Correct. Acceptance must address both stated consumers' needs.

*Review: tasks 3.7, 4.4, 4.5; R16, R17 and case 3.*

### P13 — Comparing reviews

<!-- item
  type: question
  id: P13
  answer: A
  tasks: 4.2, 4.3
  readings: R18
-->

Two review applications open the same asset revision through Hydra but show different brightness. Which investigation is most relevant first?

- **A.** Compare render delegates, camera/exposure, color settings, and composed scene state.
- **B.** Compare which application has the larger installation directory.
- **C.** Compare the order in which reviewers launched their applications.
- **D.** Compare the spelling of the supplier's publication filename.

**Answer: A**

- **A:** Correct. These are relevant inputs to a meaningful appearance comparison.
- **B:** Installation size does not explain rendering conditions.
- **C:** Launch order does not establish matching scene or display settings.
- **D:** A filename spelling comparison does not address the known same-revision rendering discrepancy.

*Review: tasks 4.2, 4.3; R18 and case 4.*

### P14 — Rendering integration assessment

<!-- item
  type: question
  id: P14
  answer: C
  tasks: 4.2, 4.3, 4.4, 4.8
  readings: R18, R22
-->

A team evaluates another renderer for an existing Hydra-based viewer. Which pilot result most directly supports adopting that integration?

- **A.** Its vendor participates in the same industry organizations as the viewer vendor.
- **B.** It opens an unrelated demonstration scene with default settings.
- **C.** It produces required outputs on representative project scenes with documented feature support.
- **D.** It produces an image file with the same dimensions as the current renderer.

**Answer: C**

- **A:** Participation is not evidence that the integration meets the project's needs.
- **B:** An unrelated example does not exercise required project features.
- **C:** Correct. Representative outputs and explicit feature evidence address suitability.
- **D:** Image dimensions test only a small part of the requirement.

*Review: tasks 4.2, 4.3, 4.4, 4.8; R18, R22 and case 4.*

### P15 — Scale and customization

<!-- item
  type: question
  id: P15
  answer: D
  tasks: 3.8, 4.6
  readings: R10, R19
-->

An installation contains many repeated fixtures with different placements. Most share internal structure; a small subset needs unique internal edits. Which plan best balances reuse and customization?

- **A.** Assume references alone guarantee shared composed structure for every copy.
- **B.** Flatten the installation before measuring its working-set requirements.
- **C.** Put every fixture behind a payload and assume this shares its internal structure.
- **D.** Evaluate instancing for the common fixtures and handle the exceptions with a suitable refinement strategy.

**Answer: D**

- **A:** Reuse through references does not alone promise the sharing associated with instancing.
- **B:** Flattening before diagnosis changes the representation without addressing the stated tradeoff.
- **C:** Payloads address loading, not the same structural-sharing requirement.
- **D:** Correct. The proposal explicitly accounts for both repeated structure and exceptions.

*Review: tasks 3.8, 4.6; R10, R19.*

### P16 — Adoption evidence

<!-- item
  type: question
  id: P16
  answer: B
  tasks: 4.1, 4.7, 4.8
  readings: -
-->

A pilot's goal is to reduce time lost reconciling mismatched asset revisions. Which evidence best supports expanding the workflow?

- **A.** A successful image from a demonstration scene unrelated to production.
- **B.** Fewer revision mismatches across repeated representative handoffs, with support effort recorded.
- **C.** A larger number of available export options in the authoring tool.
- **D.** A supplier statement that its product participates in the OpenUSD ecosystem.

**Answer: B**

- **A:** An unrelated image does not measure the target workflow problem.
- **B:** Correct. Repeated relevant results and operating effort support an adoption decision.
- **C:** More options do not establish fewer revision mismatches.
- **D:** Ecosystem participation does not establish the pilot's outcome.

*Review: tasks 4.1, 4.7, 4.8; case 4. This is a proposed evidence standard for the scenario.*

### P17 — A dimension mismatch

<!-- item
  type: question
  id: P17
  answer: C
  tasks: -
  readings: R24
-->

A museum's source asset spans 250 numeric units along its width and declares centimeters. It is referenced into a meter-based review stage with identity transforms and no conversion step. The assembled width is interpreted as 250 meters. Which change addresses the intended 2.5-meter width at that boundary?

- **A.** Save the same numeric geometry with a different USD encoding.
- **B.** Change only the source unit label to meters without changing any values.
- **C.** Apply and validate a 0.01 scale correction at the assembly boundary.
- **D.** Put the same unscaled geometry behind a payload and load it.

**Answer: C**

- **A:** Encoding changes do not reconcile the numeric dimensions.
- **B:** A label change alone leaves the stated 250-unit span uncorrected.
- **C:** Correct. Multiplying by 0.01 produces 2.5 stage units, which are meters here; validate against a known dimension.
- **D:** A loading boundary does not supply the missing geometric scale correction.

*Review: supplement S1; R24. The calculation assumes the identity transforms and missing conversion stated in the question.*

### P18 — Two delivery profiles

<!-- item
  type: question
  id: P18
  answer: A
  tasks: 4.5
  readings: R16, R25
-->

An archive receives one source model but serves both a detailed conservation viewer and a simplified visitor application. The team wants a reusable conversion path while documenting different delivery requirements. Which plan follows the two-phase exchange approach?

- **A.** Extract a faithful USD representation, then optionally transform it for each consumer.
- **B.** Simplify the source for the visitor application before preserving any detailed representation.
- **C.** Put both consumer names in metadata and assume their needs are automatically satisfied.
- **D.** Choose one consumer's structure and require every other consumer to interpret it identically.

**Answer: A**

- **A:** Correct. The extraction remains reusable, while optional transformations address each consumer's requirements.
- **B:** Early simplification can discard detail the conservation consumer needs.
- **C:** Descriptive metadata does not perform the required transformations.
- **D:** A single consumer's assumptions may not satisfy the other delivery contract.

*Review: task 4.5 and supplement S1; R16, R25.*

### P19 — Keeping a mesh type

<!-- item
  type: question
  id: P19
  answer: D
  tasks: 1.4, 1.5
  readings: R05, R27, R32
-->

A simulation consumer supports the standard collision API schema. An asset's visible surface must remain a Mesh, while its author adds collision-related properties. Which choice fits?

- **A.** Change its prim type to a material so the consumer can detect it.
- **B.** Put the word collision in the mesh's name as the complete declaration.
- **C.** Use a new file extension to make the geometry implicitly collide.
- **D.** Retain the Mesh type and apply the supported CollisionAPI schema.

**Answer: D**

- **A:** Changing the surface to an unrelated typed schema does not meet the requirement to retain a Mesh.
- **B:** A naming convention alone does not author the supported schema properties.
- **C:** File encoding does not supply collision semantics.
- **D:** Correct. The API schema adds the supported collision description while the typed prim remains a Mesh.

*Review: tasks 1.4–1.5; R05, R27, R32. A simulation consumer must still interpret the authored description.*

### P20 — A dependency outside the asset

<!-- item
  type: question
  id: P20
  answer: B
  tasks: 1.2
  readings: R03, R28
-->

A source layer defines `/Display` and a separate `/SharedLabel`. A relationship below `/Display` targets `/SharedLabel`. An assembly references only `/Display`; the external label does not appear in that composed subtree. What should the asset team investigate?

- **A.** Whether the source layer was saved more recently than the assembly layer.
- **B.** Whether the target belongs inside the asset boundary or needs an explicit assembly connection.
- **C.** Whether renaming the relationship to an attribute automatically imports its target.
- **D.** Whether packaging the unchanged source guarantees the missing subtree is composed.

**Answer: B**

- **A:** Timestamps do not extend the subtree included by a reference.
- **B:** Correct. The target is outside the included asset boundary; revise that contract or connect the dependency in the assembly.
- **C:** Changing the property category does not automatically compose the missing object.
- **D:** Packaging files does not change the reference's selected subtree.

*Review: task 1.2; R03, R28.*

### P21 — Accepting an upstream revision

<!-- item
  type: question
  id: P21
  answer: B
  tasks: 3.4, 3.6
  readings: R14, R15
-->

A supplier revises the internal parts of an installation while keeping its published root path. A downstream team has annotations and material overrides for several of those parts. What is the strongest acceptance check for adopting the revision?

- **A.** Confirm that the root path is unchanged and skip checks below it.
- **B.** Compose the revision with downstream opinions and validate their targets and intended results.
- **C.** Confirm that the new publication has a later timestamp than the previous publication.
- **D.** Flatten the earlier scene and treat that as proof the updated dependencies work.

**Answer: B**

- **A:** A stable root does not demonstrate that descendant paths, bindings or meanings are unchanged.
- **B:** Correct. It exercises the actual downstream dependency contract against the proposed revision.
- **C:** A later publication date does not establish compatibility.
- **D:** The earlier composed result does not test the revised inputs.

*Review: tasks 3.4, 3.6 and supplement S2; R14, R15 and case 5. This is a workflow acceptance recommendation.*

### P22 — A value between samples

<!-- item
  type: question
  id: P22
  answer: C
  tasks: 1.6
  readings: R06, R13, R30
-->

One float attribute has default value 90, a sample of 2 at time 0, and a sample of 10 at time 8. The stage uses linear interpolation, and there are no other value sources, blocks or offsets. What does a query at numeric time 4 return?

- **A.** 90, because a default always overrides samples from the same value source.
- **B.** 2, because this query is required to hold the earlier sample.
- **C.** 6, from interpolation between the two samples.
- **D.** No value, because a sample was not explicitly authored at time 4.

**Answer: C**

- **A:** The separate default-time value does not replace the samples for this numeric-time query.
- **B:** Holding the earlier value would be a different interpolation rule from the one specified.
- **C:** Correct. Time 4 is halfway from 0 to 8, so the result is halfway from 2 to 10: 6.
- **D:** The specified interpolation supplies a value between authored samples.

*Review: task 1.6; R06, R13, R30.*

### P23 — Two different scene costs

<!-- item
  type: question
  id: P23
  answer: A
  tasks: 3.8, 4.6
  readings: R10, R19, R26
-->

A gallery scene needs different placements for many identical display units. Profiling identifies both repeated composed structure and detail loaded during layout that nobody uses. Which investigation addresses both observations?

- **A.** Evaluate instanceable structure for repetition and payloads with a selective load policy for detail.
- **B.** Change all layer encodings and assume both kinds of cost will disappear.
- **C.** Add more variants and assume every unneeded subtree becomes independently unloadable.
- **D.** Put every opinion in a stronger layer and assume structural data becomes shared.

**Answer: A**

- **A:** Correct. The mechanisms address structural sharing and the loaded working set separately; their suitability still requires measurement.
- **B:** Encoding alone does not provide either requested behavior.
- **C:** Configuration alternatives are not a substitute for an explicit payload loading strategy.
- **D:** Stronger opinions do not by themselves create shared composed subtrees.

*Review: tasks 3.8, 4.6 and supplement S3; R10, R19, R26.*

### P24 — Preserving another consumer's data

<!-- item
  type: question
  id: P24
  answer: D
  tasks: 3.7, 4.4, 4.5
  readings: R16, R17
-->

A review tool understands geometry but does not interpret an authored inspection property. A maintenance tool needs that property after the review tool saves the asset. What should the interchange acceptance test establish?

- **A.** The review tool displays the geometry even if it discards the inspection property.
- **B.** The asset uses a smaller file encoding regardless of the retained properties.
- **C.** The inspection property can be replaced by a screenshot of its name.
- **D.** The saved asset retains the required property and the maintenance tool can read it.

**Answer: D**

- **A:** Rendering checks only the consumer that does not need the missing information.
- **B:** File size is not evidence that the required data survived.
- **C:** An image of a name does not preserve the structured property the maintenance tool consumes.
- **D:** Correct. It checks both persistence through the editing tool and usability by the downstream consumer.

*Review: tasks 3.7, 4.4–4.5; R16, R17 and case 3. Preserving data and interpreting it are distinct capabilities.*

## Reading register

| ID | Reading | Focus and boundary |
|---|---|---|
| R01 | [Stage](https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html) | Composed scene versus source documents. |
| R02 | [Attributes](https://docs.nvidia.com/learn-openusd/latest/stage-setting/properties/attributes.html) | Typed property values; skip Python details. |
| R03 | [Relationships](https://docs.nvidia.com/learn-openusd/latest/stage-setting/properties/relationships.html) | Targets connecting scene objects. |
| R04 | [OpenUSD File Formats](https://docs.nvidia.com/learn-openusd/latest/stage-setting/usd-file-formats.html) | USDA, USDC, USD, and USDZ roles. |
| R05 | [Schemas](https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/schemas.html) | Typed schemas and API schemas; conceptual distinctions. |
| R06 | [Time Codes and Time Samples](https://docs.nvidia.com/learn-openusd/latest/stage-setting/timecodes-timesamples.html) | Values over time; separate authored data from simulation behavior. |
| R07 | [Metadata](https://docs.nvidia.com/learn-openusd/latest/stage-setting/metadata.html) | Non-time-sampled information on layers, prims, and properties. |
| R08 | [Sublayers](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/what-are-sublayers.html) | Combining layer contributions at existing scene paths. |
| R09 | [References](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/references-payloads/what-are-references.html) | Reusing asset content at a destination prim. |
| R10 | [Payloads](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/references-payloads/what-are-payloads.html) | Selective loading of scene content. |
| R11 | [Variant Sets](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/variant-sets/what-are-variant-sets.html) | Authored alternatives and their selection. |
| R12 | [What Is LIVERPS?](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/strength-ordering/what-is-liverps.html) | Strength ordering; note its explicit LIVRPS/relocates transition notice. |
| R13 | [Value Resolution](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/value-resolution.html) | Resolving values from composed sources; distinguish defaults and samples. |
| R14 | [Modeling Workstreams With Layer Stacks](https://docs.nvidia.com/learn-openusd/latest/asset-structure/workstreams/modeling-workstreams.html) | Sparse contributions and ownership; layers are not a version-history system. |
| R15 | [What Is an Asset Interface?](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/asset-interface-pt1.html) | Stable public structure for downstream use. |
| R16 | [What Is Data Exchange?](https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-exchange/what-is-data-exchange.html) | Translation boundaries and information requirements. |
| R17 | [What Is Asset Validation?](https://docs.nvidia.com/learn-openusd/latest/data-exchange/asset-validation/what-is-asset-validation.html) | Validation concepts; no command memorization required. |
| R18 | [Hydra](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/hydra.html) | Scene/render separation and renderer integrations. |
| R19 | [What Is Instancing?](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/what-is-instancing.html) | Repetition, shared data, and customization tradeoffs. |
| R20 | [Custom Properties](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/custom-properties.html) | Project-specific data without immediately creating a schema. |
| R21 | [Introduction to USD; Supplemental video (YouTube)](https://openusd.org/release/intro.html) | Read “Why use USD?”, represent/compose/image sections, and capability limits. |
| R22 | [Alliance for OpenUSD](https://aousd.org/) | Mission, standardization, and ecosystem collaboration. |
| R23 | [Learn OpenUSD curriculum](https://docs.nvidia.com/learn-openusd/latest/index.html) | Optional navigation and enrichment; its development-certification scope differs from this guide. |
| R24 | [Encoding Stage Linear Units](https://openusd.org/release/api/group___usd_geom_linear_units__group.html) | Read the introductory metric and assembly rules; account for transforms rather than assuming automatic geometric conversion. |
| R25 | [Conceptual Data Mapping](https://docs.omniverse.nvidia.com/usd/latest/technical_reference/conceptual_data_mapping/index.html) | Mapping source concepts, recording transformations and documenting limitations. |
| R26 | [Scenegraph Instancing](https://openusd.org/release/api/_usd__page__scenegraph_instancing.html) | Shared descendants, editable instance-root properties and limits on descendant edits; skip API exercises. |
| R27 | [USD Physics Schema](https://openusd.org/release/api/usd_physics_page_front.html) | Representation of rigid bodies, collisions and joints; no simulator implementation required. |
| R28 | [Relationships and restrictions](https://openusd.org/release/api/class_usd_relationship.html) | Read the class description and Relationship Restrictions section; targets must remain reachable after composition. |
| R29 | [Stage flattening](https://openusd.org/release/api/class_usd_stage.html) | Read Flatten under Flatten & Export Utilities: selected variant results survive, original variant sets do not. |
| R30 | [Attribute values and interpolation](https://openusd.org/release/api/class_usd_attribute.html) | Default versus numeric-time queries, held/linear interpolation and value-source conditions. |
| R31 | [OpenUSD schema hierarchy](https://openusd.org/release/api/hierarchy.html) | Recognize UsdGeom, UsdShade, UsdLux, UsdSkel and UsdPhysics families; no hierarchy memorization required. |
| R32 | [CollisionAPI](https://openusd.org/release/api/class_usd_physics_collision_a_p_i.html) | Applied collision properties on supported geometric prims; distinguish API schemas from typed schemas. |
| R33 | [USDZ File Format Specification](https://openusd.org/release/spec_usdz.html) | Package structure and reading constraints; conceptual delivery implications only. |

