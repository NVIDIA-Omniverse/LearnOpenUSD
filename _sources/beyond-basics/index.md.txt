# Beyond the Basics

In this module, we'll go deeper into production-ready techniques that power real-world pipelines involving complex scenes, data workflows, and custom requirements across industries and use cases.

## What You'll Learn

By the end of this module, you'll understand how to:

- **Work with primvars** - attach rendering data like UVs, vertex colors, and custom attributes to geometry
- **Leverage value resolution** - understand how USD resolves attribute values from multiple composition sources
- **Create custom properties** - extend USD's data model with user-defined attributes for specific workflows  
- **Manage scene complexity** - use active/inactive prims for efficient, non-destructive scene management
- **Utilize model kinds** - structure assets using component, assembly, and group hierarchies
- **Traverse stages** - implement high-performance iteration through complex scene graphs
- **Understand Hydra rendering** - work with USD's flexible rendering architecture and multiple backends

## Why These Skills Matter

These advanced techniques separate hobby projects from production pipelines. They're the tools that enable:

- **Performance at Scale**: Handle scenes with millions of prims through efficient traversal and selective activation
- **Pipeline Flexibility**: Extend USD with custom data that fits your specific workflow needs  
- **Asset Organization**: Structure complex projects with clear hierarchies that scale across teams
- **Rendering Integration**: Connect USD scenes to any rendering backend through Hydra's extensible architecture
- **Production Robustness**: Build reliable systems that handle edge cases and complex data resolution scenarios


## What's Next

These skills prepare you for the most advanced USD topics: creating custom schemas, building specialized tools, and architecting large-scale USD-based systems, which we'll cover in the intermediate Learn OpenUSD modules.

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
:::