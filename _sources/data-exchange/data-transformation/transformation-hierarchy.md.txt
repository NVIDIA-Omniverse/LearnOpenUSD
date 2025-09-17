# Exercise: Transforming the Prim Hierarchy

In this exercise, we will create our first transformation step to turn our converted output into an asset that is easy to reference and to fix the `defaultPrim` validation error. Let's look at the tree view of a USD layer produced by `obj2usd`.

![](../../images/data-exchange/image10.png)

Notice that there are multiple prims under the stage pseudo-root (or root). While our converter output faithfully represents the flat hierarchy from OBJ, it creates two usability issues in OpenUSD:

- There is no `defaultPrim` metadata to reference this stage without specifying a target prim.
- Even with `defaultPrim` set, there's no easy way to reference the entire asset since all the prims that make up the asset don't share a common ancestor prim.

This is why we should add a transformation step to make converted OBJs easier to use out-of-box in OpenUSD. Let's choose to make this a transformation that always runs as part of our converter because it's critical to provide good UX for end users.

1. First, **open** `obj2usd.py`

2. Let’s add a new function to handle this transformation. **Copy** and **paste** this code between `extract()` and `transform()`:

```py
def set_default_prim(stage: Usd.Stage):
    """Set a default prim to make this stage referenceable

    OBJ has no notion of a scene graph hierarchy or a scene root.
    This is a mandatory chaser to move all prims under a default prim
    to make this asset referenceable.
    Args:
        stage (Usd.Stage): The stage to modify
    """

    # Get the prim in the root namespace that we want to reparent under the default prim.
    root_prims = stage.GetPseudoRoot().GetChildren()
    world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
    stage.SetDefaultPrim(world_prim)
    editor = Usd.NamespaceEditor(stage)
    for prim in root_prims:
        editor.ReparentPrim(prim, world_prim)
        editor.ApplyEdits()
```

This function creates a new `UsdGeom.Xform` prim called "/World" and sets it as the `defaultPrim`. It then parents all of the other prims in the root namespace to "/World" using `Usd.NamespaceEditor` so that they all share a common ancestor and can be referenced together.

This won’t do anything until we call the new function in `transform()`.

3. **Copy** and **paste** this code into `transform()`:

```py
set_default_prim(stage)
```

``````{dropdown} Click to reveal our Python code up to this point.
:animate: fade-in
:icon: code-square

```py
import argparse
import logging
import math
from enum import Enum
from pathlib import Path

import assimp_py
from pxr import Gf, Sdf, Tf, Usd, UsdGeom, UsdShade

logger = logging.getLogger("obj2usd")


class UpAxis(Enum):
    Y = UsdGeom.Tokens.y
    Z = UsdGeom.Tokens.z

    def __str__(self):
        return self.value

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

def extract(input_file: Path, output_file: Path) -> Usd.Stage:
    logger.info("Executing extraction phase...")
    process_flags = 0
    # Load the obj using Assimp 
    scene = assimp_py.ImportFile(str(input_file), process_flags)
    # Define the stage where the output will go 
    stage: Usd.Stage = Usd.Stage.CreateNew(str(output_file))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    # Assume linear units as meters.
    UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)

    for mesh in scene.meshes:
        # Replace any invalid characters with underscores.
        sanitized_mesh_name = Tf.MakeValidIdentifier(mesh.name)
        usd_mesh = UsdGeom.Mesh.Define(stage, f"/{sanitized_mesh_name}")
        # You can use the Vt APIs here instead of Python lists.
        # Especially keep this in mind for C++ implementations.
        face_vertex_counts = []
        face_vertex_indices = []
        for indices in mesh.indices:
            # Convert the indices to a flat list
            face_vertex_indices.extend(indices)
            # Append the number of vertices for each face
            face_vertex_counts.append(len(indices))
        
        usd_mesh.CreatePointsAttr(mesh.vertices)
        usd_mesh.CreateFaceVertexCountsAttr().Set(face_vertex_counts)
        usd_mesh.CreateFaceVertexIndicesAttr().Set(face_vertex_indices)
        # Treat the mesh as a polygonal mesh and not a subdivision surface.
        # Respect the normals or lack of normals from OBJ.
        usd_mesh.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none)
        if mesh.normals:
            usd_mesh.CreateNormalsAttr(mesh.normals)
        
        # Get the mesh's material by index
        # scene.materials is a dictionary consisting of assimp material properties
        mtl = scene.materials[mesh.material_index]
        if not mtl:
            continue
        sanitized_mat_name = Tf.MakeValidIdentifier(mtl["NAME"])
        material_path = Sdf.Path(f"/{sanitized_mat_name}")
        # Create the material prim
        material: UsdShade.Material = UsdShade.Material.Define(stage, material_path)
        # Create a UsdPreviewSurface Shader prim.
        shader: UsdShade.Shader = UsdShade.Shader.Define(stage, material_path.AppendChild("Shader"))
        shader.CreateIdAttr("UsdPreviewSurface")
        # Connect shader surface output as an output for the material graph.
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), UsdShade.Tokens.surface)
        # Get colors
        diffuse_color = mtl["COLOR_DIFFUSE"]
        emissive_color = mtl["COLOR_EMISSIVE"]
        specular_color = mtl["COLOR_SPECULAR"]
        # Convert specular shininess to roughness.
        roughness = 1 - math.sqrt(mtl["SHININESS"] / 1000.0)

        shader.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(1)
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(diffuse_color))
        shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(emissive_color))
        shader.CreateInput("specularColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(specular_color))
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(roughness)
        binding_api = UsdShade.MaterialBindingAPI.Apply(usd_mesh.GetPrim())
        binding_api.Bind(material)

    return stage


def set_default_prim(stage: Usd.Stage):
    """Set a default prim to make this stage referenceable

    OBJ has no notion of a scene graph hierarchy or a scene root.
    This is a mandatory chaser to move all prims under a default prim
    to make this asset referenceable.
    Args:
        stage (Usd.Stage): The stage to modify
    """

    # Get the prim in the root namespace that we want to reparent under the default prim.
    root_prims = stage.GetPseudoRoot().GetChildren()
    world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
    stage.SetDefaultPrim(world_prim)
    editor = Usd.NamespaceEditor(stage)
    for prim in root_prims:
        editor.ReparentPrim(prim, world_prim)
        editor.ApplyEdits()


def transform(stage: Usd.Stage, args: argparse.Namespace):
    logger.info("Executing transformation phase...")
    set_default_prim(stage)


def main(args: argparse.Namespace):
    # Extract the .obj
    stage: Usd.Stage = extract(args.input, args.output)
    # Transformations to be applied to the scene hierarchy
    transform(stage, args)
    # Save the Stage after editing
    stage.Save()

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        "obj2usd", description="An OBJ to USD converter script."
    )
    parser.add_argument("input", help="Input OBJ file", type=Path)
    parser.add_argument("-o", "--output", help="Specify an output USD file", type=Path)
    export_opts = parser.add_argument_group("Export Options")
    export_opts.add_argument(
        "-u",
        "--up-axis",
        help="Specify the up axis for the exported USD stage.",
        type=UpAxis,
        choices=list(UpAxis),
        default=UpAxis.Y,
    )

    args = parser.parse_args()
    if args.output is None:
        args.output = args.input.parent / f"{args.input.stem}.usda"

    logger.info(f"Converting {args.input}...")
    main(args)
    logger.info(f"Converted results output as: {args.output}.")
    logger.info(f"Done.")
```

``````

4. **Save** the file and **execute** the script by running the following in the terminal:

Windows:
```powershell
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj
```
Linux:
```sh
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj
```

5. **Open** the output USD stage with usdview to see the result:

Windows:
```powershell
.\scripts\usdview.bat .\data_exchange\shapes.usda
```
Linux:
```sh
./scripts/usdview.sh ./data_exchange/shapes.usda
```

You should now see in the usdview tree view that only "World" is parented under root (pseudo-root) and all of the mesh and material prims are parented under "World".

![](../../images/data-exchange/image23.png)

6. **Run** usdchecker to validate that `defaultPrim` metadata is now set:

Windows:
```powershell
.\scripts\usdchecker.bat .\data_exchange\shapes.usda
```
Linux:
```sh
./scripts/usdchecker.sh ./data_exchange/shapes.usda
```

Congratulations! No more errors reported. You've now created a fully compliant OpenUSD asset.