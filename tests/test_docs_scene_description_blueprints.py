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

"""Tests for scene-description-blueprints doc notebooks (docs/scene-description-blueprints/).

Notebooks are built to docs/_build/jupyter_execute/; paths are relative to that directory.
Each class has a full-notebook test and one test per code cell with extensive asserts.
"""

from pxr import UsdGeom

XFORM_NOTEBOOK = "scene-description-blueprints/xform.ipynb"
XFORM_SETUP = ["xform-setup"]

SCOPE_NOTEBOOK = "scene-description-blueprints/scope.ipynb"
SCOPE_SETUP = ["scope-setup"]

XFORMCOMMONAPI_NOTEBOOK = "scene-description-blueprints/xformcommonapi.ipynb"
XFORMCOMMONAPI_SETUP = ["xformcommonapi-setup"]

MATERIALS_NOTEBOOK = "scene-description-blueprints/materials-shaders.ipynb"
MATERIALS_SETUP = ["materials-setup"]

LIGHTS_NOTEBOOK = "scene-description-blueprints/lights.ipynb"
LIGHTS_SETUP = ["lights-setup"]


class TestXformNotebook:
    """Tests for scene-description-blueprints/xform.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(XFORM_NOTEBOOK)
        assert nb.stage is not None
        assert (nb._work_dir / "_assets" / "xform_prim.usda").exists()

    def test_cell_define_world(self, run_notebook):
        nb = run_notebook(XFORM_NOTEBOOK, tags=XFORM_SETUP + ["xform-define-world"])
        assert nb.stage is not None
        assert "world" in nb
        assert nb.world.GetPath() == "/World"
        assert nb.world.GetPrim().GetTypeName() == "Xform"
        assert nb.file_path == "_assets/xform_prim.usda"
        assert (nb._work_dir / "_assets" / "xform_prim.usda").exists()


class TestScopeNotebook:
    """Tests for scene-description-blueprints/scope.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(SCOPE_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "scope.usda").exists()

    def test_cell_define_scopes(self, run_notebook):
        nb = run_notebook(SCOPE_NOTEBOOK, tags=SCOPE_SETUP + ["scope-define-scopes"])
        assert nb.stage is not None
        world = nb.stage.GetPrimAtPath("/World")
        a_scope = nb.stage.GetPrimAtPath("/World/A_Scope")
        b_scope = nb.stage.GetPrimAtPath("/World/B_Scope")
        assert world.IsValid() and world.GetTypeName() == "Xform"
        assert a_scope.IsValid() and a_scope.GetTypeName() == "Scope"
        assert b_scope.IsValid() and b_scope.GetTypeName() == "Scope"
        assert not a_scope.IsActive()
        assert b_scope.IsActive()
        assert nb.stage.GetPrimAtPath("/World/B_Scope/B_Cube_0").IsValid()
        assert nb.stage.GetPrimAtPath("/World/B_Scope/B_Cube_1").IsValid()
        assert (nb._work_dir / "_assets" / "scope.usda").exists()


class TestXformCommonAPINotebook:
    """Tests for scene-description-blueprints/xformcommonapi.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(XFORMCOMMONAPI_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "xformcommonapi.usda").exists()

    def test_cell_transforms_inheritance(self, run_notebook):
        nb = run_notebook(
            XFORMCOMMONAPI_NOTEBOOK,
            tags=XFORMCOMMONAPI_SETUP + ["xformcommonapi-transforms-inheritance"],
        )
        assert nb.stage is not None
        world = nb.stage.GetPrimAtPath("/World")
        parent = nb.stage.GetPrimAtPath("/World/Parent_Prim")
        child_a = nb.stage.GetPrimAtPath("/World/Parent_Prim/Child_A")
        alt_parent = nb.stage.GetPrimAtPath("/World/Alt_Parent")
        child_b = nb.stage.GetPrimAtPath("/World/Alt_Parent/Child_B")
        assert world.IsValid() and parent.IsValid() and child_a.IsValid()
        assert alt_parent.IsValid() and child_b.IsValid()
        parent_xform = UsdGeom.Xformable(parent)
        assert parent_xform.GetXformOpOrderAttr().Get() is not None
        assert (nb._work_dir / "_assets" / "xformcommonapi.usda").exists()


class TestMaterialsShadersNotebook:
    """Tests for scene-description-blueprints/materials-shaders.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(MATERIALS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "materials.usda").exists()

    def test_cell_usdshade_material(self, run_notebook):
        nb = run_notebook(
            MATERIALS_NOTEBOOK,
            tags=MATERIALS_SETUP + ["materials-usdshade-material"],
        )
        assert nb.stage is not None
        assert nb.stage.GetDefaultPrim().GetPath() == "/World"
        box = nb.stage.GetPrimAtPath("/World/Box")
        mat = nb.stage.GetPrimAtPath("/World/Box/Materials/BoxMat")
        assert box.IsValid() and mat.IsValid()
        assert mat.GetTypeName() == "Material"
        assert (nb._work_dir / "_assets" / "materials.usda").exists()


class TestLightsNotebook:
    """Tests for scene-description-blueprints/lights.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(LIGHTS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "light_props.usda").exists()

    def test_cell_distant_light(self, run_notebook):
        nb = run_notebook(
            LIGHTS_NOTEBOOK,
            tags=LIGHTS_SETUP + ["lights-distant-light"],
        )
        assert nb.stage is not None
        sun = nb.stage.GetPrimAtPath("/World/Lights/SunLight")
        assert sun.IsValid()
        assert sun.GetTypeName() == "DistantLight"
        assert nb.stage.GetPrimAtPath("/World/Geometry/Cube").IsValid()
        assert (nb._work_dir / "_assets" / "distant_light.usda").exists()

    def test_cell_properties(self, run_notebook):
        nb = run_notebook(
            LIGHTS_NOTEBOOK,
            tags=LIGHTS_SETUP + ["lights-properties"],
        )
        assert nb.stage is not None
        sun = nb.stage.GetPrimAtPath("/Lights/Sun")
        sphere_light = nb.stage.GetPrimAtPath("/Lights/SphereLight")
        assert sun.IsValid() and sphere_light.IsValid()
        assert sun.GetTypeName() == "DistantLight"
        assert sphere_light.GetTypeName() == "SphereLight"
        # UsdLux uses inputs:color in schema; intensity is a standard attribute
        assert sun.GetAttribute("inputs:intensity").Get() == 120.0
        assert sphere_light.GetAttribute("inputs:intensity").Get() == 50000.0
        assert (nb._work_dir / "_assets" / "light_props.usda").exists()
