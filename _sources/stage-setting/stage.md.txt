---
# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Stage

Welcome to this lesson on OpenUSD stages, a core element in 3D scene description. Understanding OpenUSD stages enables collaboration across various applications and datasets by allowing us to aggregate our data in one place.

In this lesson, we will:
* Define the role of stages in 3D scene description.

## What Is a Stage?

At its core, an OpenUSD stage presents the scenegraph, which dictates what is in our scene. It is the hierarchy of objects, called prims. These prims can be anything from geometry, to materials, to lights and other organizational elements. This scene is commonly stored in a data structure of connected nodes, which is why we refer to it as the scenegraph.

```{kaltura} 1_cm4ehcvo
```

### How Does It Work?

Think of it as a scene, a shot or a scenario we may open up in a DCC. A stage could be made up entirely with just one USD file (like a robot), or it could be a USD file that includes many more USD files (like a factory with many robots). The stage is the composed result of the file or files that may contribute to a scenegraph.

Composition is the result of the algorithm for how all of the USD files (or layers, in USD parlance, as USD content need not be file-backed) should be assembled and combined. We’ll look at composition more closely later on.

![A stage with USD assets in the scenegraph.](../images/foundations/11.png)

In the example above, we have a stage, which contains USD assets in the scenegraph, like `Car.usd`, `Environment.usd`, `Lighting.usd` and `Cameras.usd`. This organization is useful for aggregating data for architectural workflows, factory planning and manufacturing, visual effects in filmmaking--anywhere where multiple assets need to be combined and integrated
seamlessly.

Each one of these USD assets can also be opened independently of the current stage. In this case, if we opened `Car.usd`, it would have its own stage that would be composed of `Simulation.usd` and `Geometry.usd`.

When we leverage OpenUSD stages properly, we can enable:

* **Modularity** : Stages enable the modification of individual elements without altering the original files (“non-destructive” editing), fostering a flexible workflow upon modular scene elements.
* **Scalability** : Stages can manage large datasets efficiently (e.g., via payloads, which we’ll learn more about when we dive deeper into composition).

### Working With Python

Creating a USD stage is the first step to generating a new USD scenegraph. In Python, we can use the functions:

```python
# Create a new, empty USD stage where 3D scenes are assembled
Usd.Stage.CreateNew()
  
# Open an existing USD file as a stage
Usd.Stage.Open()
  
# Saves all layers in a USD stage
Usd.Stage.Save()
```

## Examples

### Example 1: Create a USD File and Load it as a Stage

At its core, an OpenUSD [stage](https://openusd.org/release/glossary.html#usdglossary-stage) refers to a top-level USD file that serves as a container for organizing a hierarchy of elements called prims. Stages aren't files, but a unified scenegraph populated from multiple data sources called [layers](https://openusd.org/release/glossary.html#usdglossary-layer).

Some of the functions we will use to access the stage will be the following:
- [`Usd.Stage.CreateNew()`](https://openusd.org/release/api/class_usd_stage.html#a50c3f0a412aee9decb010787e5ca2e3e): Creates a new empty USD Stage where 3D scenes are assembled.
- [`Usd.Stage.Open()`](https://openusd.org/release/api/class_usd_stage.html#ad3e185c150ee38ae13fb76115863d108): Opens an existing USD file as a stage.
- [`Usd.Stage.Save()`](https://openusd.org/release/api/class_usd_stage.html#adefa2f7ebfc4d8c09f0cd54419aa36c4): Saves the current stage of a USD stage back to a file. If there are multiple layers in the stage, all edited layers that contribute to the stage are being saved. In our case, all edits are being done in a single layer.
   
```{code-cell}
# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Define a file path name:
file_path = "_assets/first_stage.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
print(stage.ExportToString(addSourceFileComment=False))
```

Here we created a `usda` file using Python, loaded it as a stage, and printed out the stage's contents. Since nothing is in our stage we do not get much from the output.

`.usda` are human-readable UTF-8 text. The [Crate file](https://openusd.org/release/glossary.html#crate-file-format) format is USD's own binary file format whose file extension is `.usdc` and is bi-directionally convertible to the `.usda` text format. `.usd` can refer to either Crate or text files. 


## Key Takeaways

An OpenUSD stage is the key to managing and interacting with 3D scenes using USD. The stage enables non-destructive editing, layering, and referencing, making it ideal for complex projects involving multiple collaborators. Leveraging OpenUSD stages properly can significantly enhance the efficiency
and quality of 3D content production.
