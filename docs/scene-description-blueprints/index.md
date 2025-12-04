# Scene Description Blueprints

Now that you understand USD's fundamental building blocks, it's time to learn the essential {term}`schemas <Schema>` - the blueprints that give meaning and capabilities to your {term}`prims <Prim>`. In this module, you'll discover how to use USD's built-in schemas to create the core elements of any 3D scene.

## What You'll Learn

By the end of this module, you'll be able to:

- **Define USD schemas** - understand how {term}`IsA <IsA Schema>` and {term}`API schemas <API Schema>` define what prims are and what they can do
- **Organize scenes with Scopes and Xforms** - use these organizational containers to structure complex hierarchies
- **Simplify transforms with XformCommonAPI** - use the streamlined API for common transformation workflows
- **Apply lighting schemas** - work with the UsdLux schema domain to light your scenes

## Why This Matters

These schemas provide the standardized building blocks that ensure your content works across different applications and pipelines. A prim without a schema is just an empty container; with the right schema, it becomes a light, a transform, or a piece of geometry that other applications can understand and work with.

## What's Next

After we cover essential schemas, you'll be ready to explore USD's powerful {term}`composition <Composition>` system, where you'll learn to combine and layer these building blocks into complex, collaborative scenes.

:::{toctree}
:maxdepth: 1
Overview <self>
schemas
scope
xform
xformcommonapi
lights
:::