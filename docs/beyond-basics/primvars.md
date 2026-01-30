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

# Primvars 


## What Are Primvars?

```{kaltura} 1_pqmuz40u
```

Short for {term}`primitive variables <Primvar>`, primvars are special {term}`attributes <Attribute>` that contain extra features. They address the following problems in computer graphics:

* The need to "bind" user data on {term}`geometric primitives <Gprim>` that becomes available to shaders during rendering.
* The need to specify a set of values associated with vertices or faces of a primitive that will interpolate across the primitive's surface under subdivision or shading.
* The need to inherit attributes down {term}`namespace <Namespace>` to allow sparse authoring of shareable data.

Some examples include, texture coordinates, vertex colors, or custom {term}`metadata <Metadata>`, allowing for interpolating data on individual objects.

Primvars are essential for various tasks, including:

* Storing UVs for texture mapping
* Defining vertex colors for per-vertex shading
* Deformation and animation



### How Does It Work?

Primvars are defined within the scene description and can be accessed and modified using OpenUSD APIs. Each primvar can store different types of data, such as scalar values, vectors, or arrays.

Refer to the [Primvar User Guide](inv:usd:std:doc#user_guides/primvars) to learn more about how primvars work including concepts like the different interpolation modes supported by primvars, indexed primvars, and primvar inheritance.

### Working With Python

Developers working with OpenUSD can interact with primvars using the Python API.

```python
# Constructs a UsdGeomPrimvarsAPI on UsdPrim prim
primvar_api = UsdGeom.PrimvarsAPI(prim)

# Creates a new primvar called displayColor of type Color3f[]
primvar_api.CreatePrimvar('displayColor', Sdf.ValueTypeNames.Color3fArray)

# Gets the displayColor primvar
primvar = primvar_api.GetPrimvar('displayColor')

# Sets displayColor values
primvar.Set([Gf.Vec3f(0.0, 1.0, 0.0)])

# Gets displayColor values
values = primvar.Get()
```

## Examples

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
from lousd.utils.visualization import DisplayUSD, DisplayCode
from lousd.utils.helperfunctions import create_new_stage
```

### Example 1: Primvar interpolation (constant, uniform, vertex)

This example builds the same two‑quad mesh three times and authors the displayColor primvar with three {term}`interpolation <Interpolation>` modes: constant (one value for the whole gprim), uniform (one per face), and vertex (one per point).

```{code-cell}
:emphasize-lines: 28-53
from pxr import Usd, UsdGeom, Gf

# Create stage and default prim
file_path = "_assets/primvars_displaycolor.usda"
stage = Usd.Stage.CreateNew(file_path)
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# Two-quad mesh topology (6 points, 2 faces)
mesh_vertex_locs = [
    Gf.Vec3f(-1, 0, 0),
    Gf.Vec3f(0, 0, 0),
    Gf.Vec3f(0, 1, 0),
    Gf.Vec3f(-1, 1, 0),
    Gf.Vec3f(1, 0, 0),
    Gf.Vec3f(1, 1, 0),
]
face_vertex_counts = [4, 4]
face_vertex_indices = [0, 1, 2, 3,  1, 4, 5, 2]

per_prim_color = [Gf.Vec3f(0.5, 0.0, 0.5)]
per_face_colors = [Gf.Vec3f(0.0, 0.0, 1.0), Gf.Vec3f(1.0, 0.0, 0.0)]
per_vertex_colors = [
    Gf.Vec3f(0.0, 0.0, 1.0), Gf.Vec3f(0.5, 0.0, 0.5), Gf.Vec3f(0.5, 0.0, 0.5),
    Gf.Vec3f(0.0, 0.0, 1.0), Gf.Vec3f(1.0, 0.0, 0.0), Gf.Vec3f(1.0, 0.0, 0.0)
    ]

# Define interpolation mode and colors
example_meshes = {
    "PerPrim": {
        "interpolation": UsdGeom.Tokens.constant,
        "colors": per_prim_color
    },
    "PerFace": {
        "interpolation": UsdGeom.Tokens.uniform,
        "colors": per_face_colors
    },
    "PerVertex": {
        "interpolation": UsdGeom.Tokens.vertex,
        "colors": per_vertex_colors
    }
}

for i, (example_mesh, color_details) in enumerate(example_meshes.items()):
    mesh_prim = UsdGeom.Mesh.Define(stage, world.GetPath().AppendPath(example_mesh))
    mesh_prim.CreatePointsAttr(mesh_vertex_locs)
    mesh_prim.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh_prim.CreateFaceVertexIndicesAttr(face_vertex_indices)
    UsdGeom.XformCommonAPI(mesh_prim).SetTranslate(Gf.Vec3d(i * 2.5, 0, 0))

    mesh_disp_color_primvar = mesh_prim.GetDisplayColorPrimvar()
    mesh_disp_color_primvar.SetInterpolation(color_details["interpolation"])
    mesh_disp_color_primvar.Set(color_details["colors"])

stage.Save()
```

![](../images/beyond-basics/primvar_interpolate.png)

```{code-cell}
:tags: [remove-input]
# DisplayUSD(file_path)
DisplayCode(file_path)
```

### Example 2: Store "rest state" and "deformation" as Primvars

This example writes two vertex primvars on a quad: rest_state and deformation. It computes new points as rest_state + deformation, then {term}`time samples <Time Sample>` Mesh.points

```{code-cell}
:emphasize-lines: 34-57
from pxr import Usd, UsdGeom, Sdf, Gf

# set up time sampling parameters
start_tc = 1
end_tc = 90
time_code_per_second = 30

# create stage and default prim
file_path = "_assets/primvars_mesh_deformation.usda"
stage = Usd.Stage.CreateNew(file_path)
stage.SetStartTimeCode(start_tc)
stage.SetEndTimeCode(end_tc)
stage.SetTimeCodesPerSecond(time_code_per_second)
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# define base mesh
mesh_vertex_locs = [
    Gf.Vec3f(0, 0, 0),
    Gf.Vec3f(1, 0, 0),
    Gf.Vec3f(1, 1, 0),
    Gf.Vec3f(0, 1, 0)]
face_vertex_counts = [4]
face_vertex_indices = [0, 1, 2, 3]

# create mesh prim
plane = UsdGeom.Mesh.Define(stage, world.GetPath().AppendPath("Plane"))
plane.CreatePointsAttr(mesh_vertex_locs)
plane.CreateFaceVertexCountsAttr(face_vertex_counts)
plane.CreateFaceVertexIndicesAttr(face_vertex_indices)
UsdGeom.XformCommonAPI(plane).SetTranslate(Gf.Vec3d(2, 0, 0))
plane.GetDisplayColorPrimvar().Set([Gf.Vec3f(0.1, 0.8, 0.1)])

# set the rest_state for the mesh
plane_privar_api = UsdGeom.PrimvarsAPI(plane)
plane_privar_api.CreatePrimvar(
    "rest_state",
    Sdf.ValueTypeNames.Float3Array,
    UsdGeom.Tokens.vertex).Set(mesh_vertex_locs)

# set deformation for vertex locations as a primvar
deformation = [
    Gf.Vec3f(0.0, 0.0, 0.0),
    Gf.Vec3f(-0.3, 0.4, 0.0),
    Gf.Vec3f(-0.3, 0.4, 0.0),
    Gf.Vec3f(0.0, 0.0, 0.0),
    ]
plane_privar_api = UsdGeom.PrimvarsAPI(plane)
plane_privar_api.CreatePrimvar(
    "deformation",
    Sdf.ValueTypeNames.Float3Array,
    UsdGeom.Tokens.vertex).Set(deformation)

new_points = [
    p + o for p, o in zip(
        mesh_vertex_locs,
        plane_privar_api.GetPrimvar("deformation").Get())]

print("Original vertex locations:", mesh_vertex_locs)
print("\nDeforming mesh with primvar 'deformation':", deformation)
print("\nNew vertex locations:", new_points)

# Time-sample Mesh.points from rest to deformed
plane_points = plane.GetPointsAttr()
plane_points.Set(mesh_vertex_locs, Usd.TimeCode(start_tc))
plane_points.Set(new_points, Usd.TimeCode(end_tc))

stage.Save()
```
![](../images/beyond-basics/mesh_deform.png)

```{code-cell}
:tags: [remove-input]
# DisplayUSD(file_path)
DisplayCode(file_path)
```

## Key Takeaways

The ability to store and manipulate hierarchical object data using primvars is a powerful feature that enables advanced 3D workflows and facilitates interoperability between different tools and applications. By leveraging primvars effectively, we’ll be able to efficiently manage and manipulate per-object data in complex 3D scenes, enabling advanced workflows and facilitating interoperability between different tools and applications.



