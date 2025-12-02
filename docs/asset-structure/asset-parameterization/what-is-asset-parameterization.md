# What Is Asset Parameterization?

::::{grid} auto

:::{grid-item} 
:columns: 4
:child-align: center

```{figure} ../../images/asset-structure/image49.gif
**Asset_01**
```
:::
:::{grid-item} 
:columns: 8

```{figure} ../../images/asset-structure/image39.png
```
:::

::::

{term}`Asset <Asset>` parameterization enables the reuse of content by allowing certain fields and {term}`properties <Property>` to vary downstream.

There are two primary ways to parameterize assets: {term}`variant sets <Variant Set>` and {term}`primvars <Primvar>`.

## Variant Sets

```usda
def Xform "RaceCar" (variantSets = ["color_variant"])
{
    variantSet "colorVariant" = {
        "red" { ... } 
        "blue" { ... } 
        "green" { ... } 
    }
}
```

The entry point is the first place a user goes to determine if {term}`prims <Prim>` have discrete **{term}`variants <Variant>`**. Asset structures may enforce naming conventions and require the presence of specific variants. For example, it might be expected that assets provide a `color_variant` to describe supported albedo variations.

---

## Primvars

```usda
def Xform "RaceCar" {
    color3f primvars:asset_base_color (
        doc = "primary paint color"
    )   
    color3f primvars:asset_accent_color (
        doc = "color of accent stripe"
    )   
}
```

Some variations cannot be effectively or efficiently discretized into variants. For these cases, **primvars** can be used as another form of asset parameterization. Primvars are extra parameters that can be interpolated and are primarily used to provide additional data to shading contexts. In OpenUSD, primvars are inherited down the prim hierarchy and can be authored on an ancestor prim, including the entry point of an asset.

Take, for example, the snippet above. Materials can be constructed to read `primvars:asset_base_color` or other entry point primvars. If multiple prims in a hierarchy author the same primvar, remember that child opinions are stronger than parents. We use `asset_` as a prefix to avoid {term}`namespace <Namespace>` collisions.

---

![](../../images/asset-structure/image41.png)  
Unless explicitly documented or annotated as internal, variants and primvars authored on an asset entry point should generally be considered "public" and safe for downstream contexts to edit and set, with an expectation of stability.

Both variant selection and primvars on the asset entry point are compatible with scene graph instancing. Variations in variant selections will generate new prototypes for downstream contexts, while primvars will not.

This generally makes parameterization through primvars the lighter choice for single property parameters, offering upfront memory savings at the cost of additional lookups in materials.

![](../../images/asset-structure/image20.png)  

As part of the asset prim interface, {term}`collections <Collection>` and {term}`relationships <Relationship>` can be used to indicate the membership and roles of certain prims. Consider a workflow centered around practical lights. By highlighting these practical lights in a collection at the asset entry point, it becomes easier for users to find and interact with them downstream. For example, they might want to control the intensity or turn the lights on and off.