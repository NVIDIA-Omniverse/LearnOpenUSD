# Beyond the Basics

In this module, we'll go deeper into production-ready techniques that power real-world pipelines involving complex scenes, data workflows, and custom requirements across industries and use cases.

## What You'll Learn

By the end of this module, you'll understand how to:

- **Work with {term}`primvars <Primvar>`** - attach rendering data like UVs, vertex colors, and custom attributes to geometry
- **Leverage {term}`value resolution <Value Resolution>`** - understand how USD resolves attribute values from multiple composition sources
- **Create custom {term}`properties <Property>`** - extend USD's data model with user-defined attributes for specific workflows  
- **Manage scene complexity** - use {term}`active/inactive <Active and Inactive>` {term}`prims <Prim>` for efficient, non-destructive scene management
- **Utilize {term}`model <Model>` {term}`kinds <Kind>`** - structure assets using {term}`component <Component>`, {term}`assembly <Assembly>`, and {term}`group <Group>` hierarchies
- **{term}`Traverse stages <Stage Traversal>`** - implement high-performance iteration through complex scene graphs
- **Understand {term}`Hydra <Hydra>` rendering** - work with USD's flexible rendering architecture and multiple backends
- **Handle units in USD** - work with `metersPerUnit`, `upAxis`, `timeCodesPerSecond`, and understand automatic vs. manual unit reconciliation during composition

## Why These Skills Matter

These advanced techniques separate hobby projects from production pipelines. They're the tools that enable:

- **Performance at Scale**: Handle scenes with millions of prims through efficient traversal and selective activation
- **Pipeline Flexibility**: Extend USD with custom data that fits your specific workflow needs  
- **{term}`Asset <Asset>` Organization**: Structure complex projects with clear hierarchies that scale across teams
- **Rendering Integration**: Connect USD scenes to any rendering backend through Hydra's extensible architecture
- **Production Robustness**: Build reliable systems that handle edge cases and complex data resolution scenarios


## What's Next

These skills prepare you for the most advanced USD topics: creating custom {term}`schemas <Schema>`, building specialized tools, and architecting large-scale USD-based systems, which we'll cover in the intermediate Learn OpenUSD modules.

:::{toctree}
:maxdepth: 1
Overview <self>
primvars
value-resolution
custom-properties
active-inactive-prims
model-kinds
stage-traversal
hydra
units
:::