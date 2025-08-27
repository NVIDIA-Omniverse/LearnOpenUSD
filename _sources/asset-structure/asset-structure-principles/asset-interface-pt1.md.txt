# What Is an Asset Interface?

![](../../images/asset-structure/image52.png)  

Each asset designed to be opened as a stage or added to a scene through referencing has a root layer that serves as its foundation. This root layer, known as the asset interface layer, is structured to be the primary means of interacting with the asset.

Additionally, key descendant prims within an asset, which are designated by maintainers as stable for downstream overrides, are also considered part of the asset's interface (e.g., materials or subcomponent prims). 

![](../../images/asset-structure/image21.png)

Most assets are organized around one or more defined entry point prims. These entry points act as an interface for downstream users of the composed stage, providing a clear indication of which prims are intended to be the targets of references.

A single asset entry point can typically be specified using the root layer's `defaultPrim` metadata. OpenUSD's composition engine will respect this metadata when referencing. Additionally, different domains (such as `renderSettingsPrimPath`) may introduce other methods for identifying domain-specific entry points.