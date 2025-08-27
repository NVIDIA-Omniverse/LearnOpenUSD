# Exercise: Anatomy of a Converter
Let’s create a Python script to house all our code. We'll be developing a standalone converter to help understand how a converter works.

1. Create a Python file called `obj2usd.py` in the `data_exchange` folder.

Next, we'll add some boilerplate code to help you get started. The following code is a starting point for coding the different parts of the converter. When you write your own converter, this specific structure isn't necessary.

2. Let's start with some boilerplate code:

```py

import argparse
import logging
import math
from enum import Enum
from pathlib import Path

import assimp_py
from pxr import Usd, UsdGeom

logger = logging.getLogger("obj2usd")


class UpAxis(Enum):
    Y = UsdGeom.Tokens.y
    Z = UsdGeom.Tokens.z

    def __str__(self):
        return self.value

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

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

At the top of the file, the import statements provide some interesting information. We’ll use Assimp (Open Asset Import Library), an open source file format conversion library, to parse OBJ files for us. We’re also importing the USD Python API for USD authoring.

The `if __name__ == "__main__":` section towards the bottom of the file is the entry point for the `obj2usd` script. Note that the script processes a few command line arguments:

- `input`: Takes the input OBJ file path to convert.

- `--output`: An optional output path for the exported USD file. If not supplied, it will use the OBJ file path with a `.usda` file extension instead.

- `--up-axis`: An export option to control what the up-axis for the export USD stage should be.

Once the arguments are parsed, we call `main()`. However, `main()` does not exist yet.

3. In the section `ADD CODE BELOW HERE` write the following function:

```py
def main(args: argparse.Namespace):
    # Extract the .obj
    stage: Usd.Stage = extract(args.input, args.output)
    # Transformations to be applied to the scene hierarchy
    transform(stage, args)
    # Save the Stage after editing
    stage.Save()
```

Here we’re calling two functions, `extract()` and `transform(),` which we will define in the next steps. Referring back to the anatomy of a converter, we start with the extract phase to map the data to OpenUSD as directly as possible to maintain fidelity to the source format. Then we will be performing a transformation phase which consists of one or more optional steps that are added to better meet end-client and user needs. For this module, we’ll focus on the following:

- Applying user exporting options.
- Making changes to the content structure that deviates from the source format.

4. Let’s start with defining `extract()`. Above `main(),` add the following code:

```py
def extract(input_file: Path, output_file: Path) -> Usd.Stage:
    logger.info("Executing extraction phase...")
    process_flags = 0
    # Load the obj using Assimp 
    scene = assimp_py.ImportFile(str(input_file), process_flags)
    # Define the stage where the output will go 
    stage: Usd.Stage = Usd.Stage.CreateNew(str(output_file))

    return stage
```

You’ll notice that we are not parsing through the scene data we got from Assimp. In the next module, we’ll go over how we can extract the geometry from our `.obj` file.

The last piece of our two-phase approach is defining the transformation.

5. Above `main()`, add the following code:

```py
def transform(stage: Usd.Stage, args: argparse.Namespace):
    logger.info("Executing transformation phase...")
```

At this point, we’ve outlined our two-phase process. The hierarchy is currently defined as:

- `main()` - The main entry point of our script.
  - `extract()` - Where we extract the data from `.obj` and convert it to `.usd.`
  - `transform()` - Where we apply export options and any transformations to the content structure that are not part of the original `.obj` file.

```{note} 
We will not execute the script yet, but we will continue to build upon it throughout the rest of the exercises in this module to fill out the `extract()` and `transform()` functions.
```

Below is what your python script should look like.  


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
from pxr import Usd, UsdGeom

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