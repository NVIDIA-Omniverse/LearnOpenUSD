# What Is Data Extraction?

![](../../images/data-exchange/image19.png)

## Benefits of Data Extraction

Data extraction offers several benefits:

- Output OpenUSD data "looks" like it did in the source format, making it easier to understand and debug for developers and end users. This is critical for legibility, one of the core [principles of scalable asset structure](https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html#principles-of-scalable-asset-structure-in-openusd).
- It simplifies round-tripping of data.
- It provides a common foundation for all data transformation in the transform phase.

## Transient Data

The output USD data from the data extraction phase is often treated as transient data. The author of an exporter will often choose to not write the data extraction output to disk and only output the transformed data which is better-suited for end users.

Authors of data exchange implementations should consider optionally giving access to the in-memory extracted stage or writing the extracted stage to disk as it is valuable for third party developers that may want to write their own transformation steps. Without it, third party developers may be left to reverse engineer your transformations.

Examples of transient data from the extraction phase that could be useful during the transformation phase include:

- **Texture and Material conversion**
  - When converting between formats like FBX and glTF, materials or textures may need to be converted from one format’s structure to another. For instance, an FBX material may contain complex shader information not supported by glTF.
  - Transient data in such a case may take the form of intermediate texture maps, shader definitions, or color values that help map FBX materials to glTF ones. This data may be discarded after conversion, or cached in order to be reused for repeated iterations, or during development.
- **Metadata information**
  - CAD files might contain extensive metadata related to manufacturing (e.g. BIM metadata about material properties, tolerances, or design notes) which may not be relevant for real-time visualization or rendering applications.
  - Transient metadata may take the form of filters tagging the information to retain, or sidecar files such as JSON, XML, PDF or Excel containing the annotations originally included in the source files.
- **Level of Detail (LoD) conversion**
  - Formats such as FBX or CAD may store multiple levels of detail for a model. As OpenUSD or target output formats do not universally offer out-of-the-box support for LoDs, a specific geometry LoD must be selected by the transformation process.
  - In this scenario, intermediate mesh representations or LoD selection metadata may be persisted to disk for use at a later time. These may be carried along the pipeline for downstream use, or discarded at the end of the process.

## Conceptual Data Mapping

![](../../images/data-exchange/image18.png)

To achieve a direct and faithful extraction between two data formats, conceptual data mapping is crucial. This process involves analyzing how to map data models from one format to another. You'll find many commonalities that make for easy extraction, but you may also identify scene description schema gaps (i.e. data models from other formats that don’t map directly to any concepts in USD). Identifying and proposing new schemas for OpenUSD helps enrich the interchange of our scene descriptions and grow the OpenUSD ecosystem.

Producing a conceptual data mapping document as you go through this process can be valuable:

- It serves as a data specification for your extraction implementation and helps stakeholders participate in setting requirements and expectations.
- Stakeholders should strive to keep their document up-to-date with:
  - Changes to the source data format
  - Changes to OpenUSD
  - Changes to an official data mapping implementation
- The document enables effective discourse when asking for feedback from the OpenUSD community or communicating schema gaps.
- It helps third-party developers understand which features are supported between the two formats and what to expect from the extraction phase, allowing them to develop their own data transformations.

The image shows a conceptual data mapping document created for the `obj2usd` converter we're developing in this module. Other examples, like the USD and MaterialX concept mapping, can be found in the [OpenUSD documentation](https://openusd.org/release/api/usd_mtlx_page_front.html#usdMtlx_concepts). You can also checkout our additional [guidance and template for conceptual data mapping](https://docs.omniverse.nvidia.com/usd/latest/technical_reference/conceptual_data_mapping/index.html). We hope to see many more conceptual data mapping documents in the future.

![](../../images/data-exchange/image22.png)

Here is an example of how data is extracted from an OBJ file and mapped to OpenUSD. Let’s try this mapping first hand with the next exercise.