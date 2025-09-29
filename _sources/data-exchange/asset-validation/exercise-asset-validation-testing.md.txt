# Exercise: Asset Validation and Testing

OpenUSD is incredibly powerful and flexible. As you develop your data exchange implementation, you can test it against different test assets and also use validators like usdchecker to make sure that your implementation is authoring valid and compliant OpenUSD data. In this exercise, we will use usdchecker to find any issues with an asset output by our `obj2usd` converter and improve our code accordingly.

1. Let's get a fresh conversion from `obj2usd` to validate. Execute the script by running the following in the terminal.

Windows:
```powershell
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj
```
Linux:
```sh
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj
```

2. Now, let's run usdchecker to see what issues we find with our asset.

Windows:
```powershell
.\scripts\usdchecker.bat .\data_exchange\shapes.usda
```
Linux:
```sh
./scripts/usdchecker.sh ./data_exchange/shapes.usda
```

usdchecker reports three errors for our asset, all related to stage metadata:

![](../../images/data-exchange/image32.png)

Our asset is missing metadata specifying the `upAxis` and units type for linear units. We should fix these now in our converter, as this was an oversight in the extraction phase. The missing `defaultPrim` metadata is better handled during the transformation phase, but it's good that usdchecker is flagging it for us.

3. Open `obj2usd.py`.

1. Let's set the `upAxis` and `metersPerUnit` stage metadata to fix the errors we encountered. Copy and paste this code in `extract()` after we define `stage`.

```py
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# Assume linear units as meters.
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.meters)
```

The OBJ specification states that the Y axis is the `upAxis` in OBJ files, so we can map that directly to OpenUSD. For linear units, OBJ is unitless. For our converter, we'll choose meters as a sensible default. Note that the API for this geometric stage metadata is found in `UsdGeom`, not `Usd.Stage` where you might first think to look for it.

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


def transform(stage: Usd.Stage, args: argparse.Namespace):
    logger.info("Executing transformation phase...")


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

5. Run the script again to generate a fixed asset.

Windows:
```powershell
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj
```
Linux:
```sh
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj
```


6. Let’s see what usdchecker reports now. Run usdchecker.

Windows:
```powershell
.\scripts\usdchecker.bat .\data_exchange\shapes.usda
```
Linux:
```sh
./scripts/usdchecker.sh ./data_exchange/shapes.usda
```

We are down to one error.

![](../../images/data-exchange/image25.png)

We successfully fixed both the `upAxis` and `metersPerUnit` errors in our asset by updating our `obj2usd` code. We'll fix the `defaultPrim` issue in the next exercise when we dive into the transformation phase.