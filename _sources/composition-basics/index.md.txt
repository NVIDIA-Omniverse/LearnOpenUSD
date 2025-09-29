# Composition Basics

This module introduces you to USD's composition system - the technology that makes collaborative, non-destructive, and modular 3D workflows possible. Here you'll discover how to combine, layer, and reference scene elements to build complex projects that scale from individual assets to entire virtual worlds.

## What You'll Learn

By the end of this module, you'll be able to:

- **Understand layers and composition** - learn how USD combines multiple data sources into unified scenes
- **Navigate strength ordering (LIVRPS)** - understand the rules that determine which data takes precedence when conflicts arise
- **Use specifiers effectively** - control how prims are interpreted with `def`, `over`, and `class` specifiers
- **Create modular assets with references** - build reusable components that can be shared across projects
- **Set default prims** - establish clear entry points for your composed assets
- **Implement variant sets** - create multiple variations of assets that can be swapped at runtime

## Why This Matters

USD's composition system is what transforms it from just a 3D file format into a complete collaborative platform. Instead of traditional "destructive" editing where changes overwrite original data, USD enables:

- **Non-Destructive Workflows**: Make changes in separate layers without affecting source data
- **Real-Time Collaboration**: Multiple artists can work on the same scene simultaneously
- **Asset Reuse**: Create once, reference everywhere - from single assets to large assemblies 
- **Variant Management**: Switch between different versions, LODs, or configurations on demand
- **Scalable Pipelines**: Build scenes that can reference thousands of assets efficiently


## What's Next

After mastering composition basics, we'll explore techniques like using payloads for performance optimization and specialized workflows for complex production scenarios.

:::{toctree}
:maxdepth: 1
Overview <self>
layers
strength-ordering
specifiers
references
default-prim
variant-sets
:::