# What Is Data Transformation?

![](../../images/data-exchange/image12.png)

Data transformation allows customers to tailor data to their specific needs. While DCC developers should ideally handle data extraction, they can leave transformation open for third-party developers to extend.

Key aspects of data transformation include:

- Export options
- Content re-structuring
- Optimizations, e.g., mesh merging

As OpenUSD expands into new industries and domains, your exporter must adapt to meet evolving requirements. This flexibility ensures your OpenUSD export can easily accommodate future use cases and demands.

## Reusability of Transformation Code

Export options, optimizations and {term}`asset <Asset>` structure code can be shared across applications since they all operate on OpenUSD data. While extraction code from source formats to OpenUSD is largely unique, data transformation for specific clients or workflows can be designed for reuse across multiple exporters.



## DCC Exporters

DCC exporters should create transformations to provide a positive experience for predominant user workflows. If most of your users want to export OpenUSD for a 3D configurator in a game engine, make it work out of the box so they don't need a developer.

![](../../images/data-exchange/image9.png)

At the same time, provide a transformation pipeline so developers can choose which of your data transformations they want to use and even add their own.

## Round-Trip Data Exchange

![](../../images/data-exchange/image8.png)

When designing workflows that involve round-trip data exchange (importing and exporting), minimize data transformations. Extensive transformations can complicate the process of accurately reversing changes when reimporting the data, potentially leading to loss of information or inconsistencies.

## Data Transformation Opportunities

![](../../images/data-exchange/image21.png)

Transformation is also a good time to prune data that may not be relevant to a workflow or client.

Conversely, third-party developers may want to add more data to an export or extract additional data that is currently not supported by the extraction implementation. This could be handled in an early step in the transformation pipeline.

Third-party developers can leverage the {term}`stage <Stage>` from the raw extraction to export the data as sparse {term}`overrides <Over>` if they choose for multi-workstream workflows.

![](../../images/data-exchange/image14.png)

A transformation step doesn't need to happen in the same process as extraction or other transformation steps. It could be a separate process or a cloud service. You can even consider transformations that may occur as post-processes after a stage has been exported or converted.

![](../../images/data-exchange/image11.png)

Based on their experience with exporting other file formats, most end users typically expect a single-file export. In most cases, it makes sense for that to be your default export.

In practice, most organizations have an established asset structure, and the export will need to be transformed to fit that structure.

Asset structures might leverage one or more OpenUSD concepts like {term}`composition <Composition>`, asset parameterization and workstreams.

If the export is just one workstream of a larger asset structure, it could be additive and define new {term}`prims <Prim>`, apply overrides on existing prims, or both. The exporter needs to be able to take the data extraction and distill it down to that workstream's unique contributions.

Many exporters include export options to provide users with greater flexibility and control over the export. Some options may consist of choices users need to make to conform to the destination format, and other options may be added to support various workflow requirements for users.

It's good practice to think of export options as data transformation and not as part of extraction.