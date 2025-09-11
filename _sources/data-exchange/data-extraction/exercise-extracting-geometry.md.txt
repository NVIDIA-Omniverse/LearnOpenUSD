# Exercise: Extracting Geometry

Now that we have a way to parse the data in our `.obj` file, we can start extracting the information and translating it into OpenUSD. When parsing through each mesh in the scene, we need to make sure the mesh name can be used as an identifier or prim name.

1. Let's add the Tools Foundation library to our `pxr` imports. At the top of the file, add `Tf` to the list of imports from `pxr`. It should look like this:

```py
from pxr import Tf, Usd, UsdGeom
```

2. Next, let's add to our `extract()` method. Right underneath where we defined stage and before we call `return stage`, we'll add our initial loop to go through all meshes in the scene. In OpenUSD, we need to ensure the mesh identifier is valid before we define it in our stage.

```{attention}
Pay attention to your indentations if you are copying and pasting.
```

```py
for mesh in scene.meshes:
    # Replace any invalid characters with underscores.
    sanitized_mesh_name = Tf.MakeValidIdentifier(mesh.name)
    usd_mesh = UsdGeom.Mesh.Define(stage, f"/{sanitized_mesh_name}")
```

Based on the diagram below, we'll first extract the vertex indices of the face and the number of vertices for each face from our object.

![](../../images/data-exchange/image6.png)

3. Still within our loop, we'll create another loop to go through each vertex index for each mesh. This allows us to assemble both the face vertex indices and the face vertex count arrays for `UsdGeom.Mesh`. Add the following code underneath where we defined `usd_mesh`:

```py

# You can use the Vt APIs here instead of Python lists.
# Especially keep this in mind for C++ implementations.
face_vertex_counts = []
face_vertex_indices = []
for indices in mesh.indices:
    # Convert the indices to a flat list
    face_vertex_indices.extend(indices)
    # Append the number of vertices for each face
    face_vertex_counts.append(len(indices))
```

![](../../images/data-exchange/image3.png)

Both OBJ and OpenUSD store lists of vertices and lists of faces that reference their member vertices by index. OBJ keeps one global list of vertices for all objects, whereas OpenUSD tracks vertices on a per-mesh basis. Fortunately, Assimp has already taken care of mapping the global vertices of OBJ to per-mesh.

Another difference to note is that the indices from OBJ are grouped on a per-face basis, but OpenUSD prefers a flattened list of indices that can be recomposed into faces using an ordered list of face vertex counts. For an example, compare the `faces` and `faceVertexIndices` arrays in the image above.

This code accomplishes two things:

- It flattens the per-face indices into one continuous list.
- For each face, it counts how many indices it's made up of to populate the list of face vertex counts.

4. Now, with the rest of the information from Assimp, we can create the attributes to define the points, faces and normals of the meshes in OpenUSD. Let's add the following code to create these attributes. Place the code after our last loop but not inside of it.

```py

usd_mesh.CreatePointsAttr(mesh.vertices)
usd_mesh.CreateFaceVertexCountsAttr().Set(face_vertex_counts)
usd_mesh.CreateFaceVertexIndicesAttr().Set(face_vertex_indices)
# Treat the mesh as a polygonal mesh and not a subdivision surface.
# Respect the normals or lack of normals from OBJ.
usd_mesh.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none)
if mesh.normals:
    usd_mesh.CreateNormalsAttr(mesh.normals)
```

It’s worth noting here that we’re setting the attribute values in two different ways:

- The points attribute is set by passing a default value in the `CreatePointsAttr()`.
- `faceVertexCounts` is set by calling `Set()` using the `UsdAttribute` object returned by `CreateFaceVertexCountsAttr()`.

Both ways are available and valid. Calling `Set()` opens up the opportunity to set timeSamples if you need to. Also note that we are setting the subdivision scheme to `UsdGeom.Tokens.none` so that these meshes are explicitly treated as polygonal meshes, not SubD meshes, as OBJ doesn’t support SubD meshes.

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
from pxr import Tf, Usd, UsdGeom

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

5. From here we can save the file and execute the script on our `shapes.obj` file. Run the following in the terminal:

Windows:

```
python .\data_exchange\obj2usd.py .\data_exchange\shapes.obj
```

Linux:

```
python ./data_exchange/obj2usd.py ./data_exchange/shapes.obj
```

6. We can use usdview to see the results. Execute the following command in the terminal:

Windows:

```
.\scripts\usdview.bat .\data_exchange\shapes.usda
```

Linux:

```
./scripts/usdview.sh ./data_exchange/shapes.usda
```

You should now see the three shapes in the viewport. Notice that the artistic intent for the normals is preserved. The sphere has smooth normals, but the cone is faceted.

![](../../images/data-exchange/image16.png)