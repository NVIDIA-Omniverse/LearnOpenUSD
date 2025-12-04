# OpenUSD File Formats

In this lesson, we'll explore the core OpenUSD file formats – USD, USDA, USDC and USDZ. All the formats are used by OpenUSD for storing and exchanging 3D scene data of various types, including meshes, cameras, lights, and shaders.

```{kaltura} 1_dl84ev5g
```

## What Is USDA?

USDA (`.usda`) are ASCII text files that encode scene descriptions in a format that can easily be read and edited. It is a native file format used by OpenUSD to store and exchange 3D scene data. It is human‑readable, which makes USDA particularly useful for tasks that involve manual editing or inspection of
scene data. This makes USDA optimal for small files, such as a {term}`stage <Stage>` that is referencing external content.

## What Is USDC?

The {term}`Crate Binary Format <Crate File Format>`, or USDC (`.usdc`), is a compressed binary file format used by OpenUSD to store and exchange 3D scene data. It is designed to minimize load time and provide a more efficient representation of the scene data compared to the human‑readable ASCII format (USDA).

The Crate Binary Format uses various compression techniques to reduce the file size and improve loading performance. It also employs memory mapping for faster file access and loading times. The structure of the file is organized in a way that allows for efficient parsing and retrieval of the scene data. USDC is extremely efficient for numerically-heavy data, like geometry.

## What Is USD?

A USD (`.usd`) file can be either ASCII or binary – the advantage of which is that we can change the underlying format at any point without breaking {term}`references <Reference>`. Using USD is also beneficial for debugging, because an {term}`asset <Asset>` that is in binary can easily be changed to ASCII to take a look at what might be causing the issue. As we learn more about USD, we may decide to separate
heavier data from more light weight data. When doing so, consider using `.usdc` and `.usda` explicitly to avoid obfuscation and create large `.usda` files unintentionally.

## What Is USDZ?

Let’s also touch on USDZ (`.usdz`). USDZ is an atomic, uncompressed, zipped archive so that we can deliver all of the necessary assets together. We would not use USDZ if we are still making edits to the asset, but it is a great way to package and ship our asset when it is complete. For example, a mesh with its texture files can be delivered as one archive. It’s generally intended as read‑only and is optimal for XR experiences. More on USDZ will be covered in future lessons.

---

Each USD file format can be created through Python bindings in the OpenUSD library. When creating a new stage we can pass in a string to represent a file name that ends in `.usdc`, `.usd`, `.usda`, or `.usdz`.

In these lessons, we primarily use USDA files because they are human-readable, making them ideal for learning and accessibility. As you advance in your OpenUSD work, you may prefer to use USDC or USD formats instead.

```{note}
The file formats used in these lessons are chosen for clarity. In production, follow the OpenUSD guidance for production use cases, which includes:
* Prefer the binary usdc format (often saved with the .usd extension) for {term}`layers <Layer>` that contain data‑heavy content such as geometry or shading networks, because it opens faster and uses less memory.
* Reserve usda text for small, human‑readable “interface” layers that mostly reference or sublayer other files, and for debugging or diffing.
* In general, “prefer crate files” for big data, and keep text to lightweight aggregators.

[See Maximizing USD Performance for the full recommendations](https://openusd.org/release/maxperf.html).

```

## Key Takeaways

Now, we should have a better understanding of the various OpenUSD file formats and the purpose each one serves.

* There are four native formats: USD, USDA, USDC and USDZ and they are used by OpenUSD for storing and exchanging 3D scene data.
* All OpenUSD file formats are hierarchical and extensible based on layers and {term}`composition <Composition>`, which supports non‑destructive editing, collaboration, and interoperability between different software tools.
* Any other 3D file format can be loaded into OpenUSD Stages through plugins. It’s worth noting that any data provider can implement file format plugins to natively speak USD – even `.usdc`, `.usd`, `.usda`, and `.usdz` are file format plugins.
* Developers can interact with USD files using Python bindings.



