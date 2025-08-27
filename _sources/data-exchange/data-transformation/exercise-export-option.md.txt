# Exercise: Adding an Export Option

Previously, we added a core mandatory transformation step to our `obj2usd` converter to make it easier to reference our converted assets. End users may not want or need all of the available transformation steps. For this exercise, we will add a new transformation step in the form of an export option so that end users can choose whether to apply the transformation on conversion or not.

We will utilize the `--up-axis` command-line flag to allow end users to change the `upAxis` upon conversion to OpenUSD. This is desirable because even though OBJ is Y-up, the rest of an organization's pipeline might be Z-up, and they would prefer that the output conforms to their pipeline.

1. **Open** `obj2usd.py`

2. Let’s add a new function to handle this `--up-axis` export option and apply the transformation. **Copy** and **paste** this code between `set_default_prim()` and `transform()`:

```py
def set_up_axis(stage: Usd.Stage, up_axis: UpAxis):
    """Set the specified up-axis for the stage.

    OBJ is Y-up by default. This is an optional chaser to allow
    users to change the up-axis to suit their pipeline. Corrective
    transformations are applied.

    Args:
        stage (Usd.Stage): The stage to modify
        up_axis (UpAxis): The up-axis value to set.
    """
    if up_axis == UpAxis.Y:
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    else:
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        xformable = UsdGeom.Xformable(stage.GetDefaultPrim())
        xformable.AddRotateXOp(opSuffix="unitsResolve").Set(90.0)
```

This function sets the `upAxis` metadata accordingly. If the `upAxis` is not the OBJ default (Y), it will also apply a corrective on the `defaultPrim` to reorient the stage to remain face up in the new coordinate system. We suffix the X-axis rotation operation with "`unitsResolve`" by convention to explain to end users the purpose of the transformation.

This won’t do anything until we call the new function in `transform()`.

3. **Copy** and **paste** this code into `transform()`:

```py
set_up_axis(stage, args.up_axis)
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


def set_up_axis(stage: Usd.Stage, up_axis: UpAxis):
    """Set the specified up-axis for the stage.

    OBJ is Y-up by default. This is an optional chaser to allow
    users to change the up-axis to suit their pipeline. Corrective
    transformations are applied.

    Args:
        stage (Usd.Stage): The stage to modify
        up_axis (UpAxis): The up-axis value to set.
    """
    if up_axis == UpAxis.Y:
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    else:
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        xformable = UsdGeom.Xformable(stage.GetDefaultPrim())
        xformable.AddRotateXOp(opSuffix="unitsResolve").Set(90.0)


def transform(stage: Usd.Stage, args: argparse.Namespace):
    logger.info("Executing transformation phase...")
    set_default_prim(stage)
    set_up_axis(stage, args.up_axis)


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
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj --up-axis Z
```
Linux:
```sh
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj --up-axis Z
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

6. **Click** on "root" in the usdview tree view.

![](../../images/data-exchange/image15.png)

In the *Meta Data* tab, you can confirm now that `upAxis` is set to `Z`.

7. **Click** on "World" in the tree view.

![](../../images/data-exchange/image24.png)

In the *Properties* panel, you can see the `xformOp:rotateX:unitsResolve` applying the corrective to keep the shapes upright despite the new `upAxis`.