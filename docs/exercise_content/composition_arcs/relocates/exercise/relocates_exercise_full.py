# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

from pathlib import Path

from pxr import Usd, Sdf, UsdGeom


working_dir = Path(__file__).parent

stage = Usd.Stage.CreateNew(str(working_dir / "main_street_signage.usda"))
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# Reference the vendor asset. We cannot edit signage_asset.usd, so any naming
# cleanup has to happen here, in our own layer stack.
sign = stage.DefinePrim("/World/Sign_01", "Xform")
sign.GetReferences().AddReference("./signage_asset.usd")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Relocates are layer metadata, so they are authored on the layer rather than
# on a prim. Each entry maps a source path to a target path.
stage.GetRootLayer().relocates = [
    # Part 1: rename the mesh prims to match our pipeline's naming convention.
    (Sdf.Path("/World/Sign_01/sign_MESH_01"), Sdf.Path("/World/Sign_01/sign")),
    (Sdf.Path("/World/Sign_01/post_MESH_01"), Sdf.Path("/World/Sign_01/post")),
    # Part 2: relocating to an empty path removes the prim from the stage.
    (Sdf.Path("/World/Sign_01/tmp_rig_helper"), Sdf.Path.emptyPath),
]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()
