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
# Default Prim

In this lesson, we’ll explore the concept of default prims in Universal Scene Description. Default prims are essential for scene management, especially when dealing with complex hierarchies and {term}`references <Reference>`. By the end of this lesson, we’ll understand what default prims are, why they are important, and how to set them using Python.

## What Is a Default Prim?

![Default Prim Definition](../images/foundations/DefaultPrim_Definition.webm)
A default prim in OpenUSD is a top-level {term}`prim <Prim>`, or primitive, that is part of the {term}`layer <Layer>` {term}`metadata <Metadata>` and serves as the primary entry point or root for a {term}`stage <Stage>`. It helps other parts of the system know where to start or what to focus on.


### How Does It Work?

It is best practice to set a default prim in our stages. This is crucial for tools and applications that read USD files, as it guides them to the primary content; for some it may even be considered invalid if the default prim is not specified for the stage. `usdchecker` checks for a default prim and reports an error if it is not set on a stage. A default prim is also particularly useful when the stage’s root layer is referenced in other stages (such as a reference or {term}`payload <Payload>`), as it eliminates the need for consumers to specify a target prim manually.

Let’s look at this example. Let's assume we have a USD file named `simple_scene.usda` with the following content:
```usda
#usda 1.0
(
    defaultPrim = "Car"
)

def Xform "Car" {
    def Mesh "Body" {
        double3[] points = [(0, 0, 0), (2, 0, 0), (2, 1, 0), (0, 1, 0)]
        int[] faceVertexCounts = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]
    }
}

def Xform "Building" {
    def Mesh "Structure" {
        double3[] points = [(0, 0, 0), (5, 0, 0), (5, 10, 0), (0, 10, 0)]
        int[] faceVertexCounts = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]
    }
}
```

The `defaultPrim` metadata is set to "Car", indicating that "Car" is the main entry point of this USD file. When we bring this `.usda` in as a reference or payload the "Car" will show up visually in the stage. If we set the `defaultPrim` to "Building" then the "Building" will show up in the stage when referenced. If no `defaultPrim` is set then when the above `.usda` is brought in as a payload or reference it will resolve as an empty layer and output a warning message in the log.

### Working With Python

![Default Prim Python](../images/foundations/DefaultPrim_Python.webm)

The default prim is set using the `SetDefaultPrim()` method on a USD stage. This method accepts any `Usd.Prim`, but the prim must be a top-level prim on the stage. Here’s a simple example:

```python
from pxr import Usd, UsdGeom, Sdf

# Create a new USD stage
stage = Usd.Stage.CreateInMemory()

# Define a top-level Xform prim
default_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()

# Set the Xform prim as the default prim
stage.SetDefaultPrim(default_prim)

# Export the stage to a string to verify
usda = stage.GetRootLayer().ExportToString()
print(usda)

# Check that the expected default prim was set
assert stage.GetDefaultPrim() == default_prim
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from utils.visualization import DisplayUSD, DisplayCode
```

### Example 1: Setting a Default Prim

[`SetDefaultPrim()`](https://openusd.org/release/api/class_usd_stage.html#a82b260faf91fbf721b0503075f2861e2) sets the default prim for the stage's root layer.

A `defaultPrim` is layer metadata. If the stage's root layer is used as a reference or payload it is best practice to set a default prim.


```{code-cell}
:emphasize-lines: 9-10

from pxr import Usd

file_path = "_assets/default_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
stage.DefinePrim("/hello")
stage.DefinePrim("/hello/world")
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")

# Set the default primitive of the stage to the primitive at "/hello":
stage.SetDefaultPrim(hello_prim)

stage.Save()
```
```{code-cell}
:tags: [remove-input]
DisplayCode(file_path)
```

## Key Takeaways

In summary, a default prim is the top-level prim that serves as the main entry point for a USD stage. Setting a default prim is a best practice when our stage’s root layer might be composed into another stage, whether as a reference or a payload.

By utilizing default prims, we can create more organized and manageable USD stages.



