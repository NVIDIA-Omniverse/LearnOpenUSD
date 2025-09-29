# Exercise: Extracting Materials

Similar to how we extracted the geometry from our `.obj` file, we will now extract the materials. This is the last part of the code that we will be adding to `extract()`.

1. At the top of our file, add `Gf`, `Sdf`, and `UsdShade` imports from `pxr`.

```py
from pxr import Gf, Sdf, Tf, Usd, UsdGeom, UsdShade
```

Here we'll sanitize the material identifiers as we did with the meshes. Then we'll set up the initial shaders.

2. Let’s get each material from the mesh. Add the following code to get the material and check if it exists before creating the identifier. This will slot underneath where we defined our `if mesh.normals` but not inside the if statement.

```py
# Get the mesh's material by index
# scene.materials is a dictionary consisting of assimp material properties
mtl = scene.materials[mesh.material_index]
if not mtl:
    continue
sanitized_mat_name = Tf.MakeValidIdentifier(mtl["NAME"])
material_path = Sdf.Path(f"/{sanitized_mat_name}")
```

3. Next, we will create the material prim in our stage that has a shader surface for the material graph. Add the following code underneath `material_path`.

```py
# Create the material prim
material: UsdShade.Material = UsdShade.Material.Define(stage, material_path)
# Create a UsdPreviewSurface Shader prim.
shader: UsdShade.Shader = UsdShade.Shader.Define(stage, material_path.AppendChild("Shader"))
shader.CreateIdAttr("UsdPreviewSurface")
# Connect shader surface output as an output for the material graph.
material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), UsdShade.Tokens.surface)
```

First, we get the material info from Assimp using the material index stored with the mesh. You'll notice that we ensure we're using a valid identifier for the material name. With the valid material name, we create the `UsdShade.Material` and `UsdShade.Shader`.

The material prim serves as a container for a material graph. In this case, we have just one node in our material graph, a `UsdPreviewSurface` shader. Lastly, we loft the material graph output by connecting the `outputs:surface` from the shader prim to the material prim.

4. Save the file and execute the script by running the following in the terminal.

Windows:

```
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj

```

Linux:

```
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj
```

5. Open the output USD stage with usdview to see the result.

Windows:

```
.\scripts\usdview.bat .\data_exchange\shapes.usda
```

Linux:

```
./scripts/usdview.sh ./data_exchange/shapes.usda
```

6. With usdview open, click on the `Material_001` prim in the stage tree and expand `outputs:surface` in the *Properties* window.

![](../../images/data-exchange/image34.png)

```{attention}
If you don't see the following in usdview, make sure **Default Dome Light** is enabled. You can enable it by going to **Lights > Enable Default Dome Light**.
```

![](../../images/data-exchange/image4.png)

We've defined the material graph and primary shader for each material, but at this point, you shouldn't see any visual difference in the viewport.

One point of interest is that the material names were fixed in this case with `Tf.MakeValidIdentifier()` since this OBJ was authored in Blender with material names in the format: “Material.001”. The invalid character, the period, was replaced with an underscore. You can open the OBJ file in VS Code to see the original material names. Additionally, the expanded `outputs:surface` property on the material prim shows the connection to the shader prim.

7. Next, let’s map the material properties from OBJ to the `UsdPreviewSurface` shader. Copy and paste this code below where we created our shaders.

```py
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
```

Here we are setting the `UsdPreviewSurface` shader to use a specular workflow instead of PBR, as it maps most directly to the data coming from OBJ. After that, we create the relevant inputs and set their values from OBJ. This will complete the material definitions, but we won't see anything in the viewport until we bind the material to the mesh.

8. Let’s bind the material to the mesh. Add the following code below the shader connections, `shader.CreateInput()`.

```py
binding_api = UsdShade.MaterialBindingAPI.Apply(usd_mesh.GetPrim())
binding_api.Bind(material)
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

9. Save the file and execute the script by running the following in the terminal.

Windows:
```
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj
```
Linux:
```
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj
```

10. Open the output USD stage with usdview to see the result:

Windows:
```
.\scripts\usdview.bat .\data_exchange\shapes.usda
```

Linux:
```
./scripts/usdview.sh ./data_exchange/shapes.usda
```

Now, we should see unique materials on the meshes.

![](../../images/data-exchange/image5.png)

Notice the diffuse and specular differences between the materials. Take some time to explore the values on the different shaders and their visual results in the viewport.