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

"""Tests for composition-basics doc notebooks (docs/composition-basics/).

Notebooks are built to docs/_build/jupyter_execute/; paths are relative to that directory.
Each class has a full-notebook test and one test per code cell with extensive asserts.
"""

from pxr import Sdf
import pytest

SPECIFIERS_NOTEBOOK = "composition-basics/specifiers.ipynb"
SPECIFIERS_SETUP = ["specifiers-setup"]

REFERENCES_NOTEBOOK = "composition-basics/references.ipynb"
REFERENCES_SETUP = ["references-setup"]

DEFAULT_PRIM_NOTEBOOK = "composition-basics/default-prim.ipynb"
DEFAULT_PRIM_SETUP = ["default-prim-setup"]


class TestSpecifiersNotebook:
    """Tests for composition-basics/specifiers.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(SPECIFIERS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "specifiers_over_base.usda").exists()

    def test_cell_def_and_class(self, run_notebook):
        nb = run_notebook(
            SPECIFIERS_NOTEBOOK,
            tags=SPECIFIERS_SETUP + ["specifiers-def-and-class"],
        )
        assert nb.stage is not None
        box = nb.stage.GetPrimAtPath("/World/Box")
        box_2 = nb.stage.GetPrimAtPath("/World/Box_2")
        class_prim = nb.stage.GetPrimAtPath("/World/_Look/_green")
        assert box.IsValid() and box.GetSpecifier() == Sdf.SpecifierDef
        assert box_2.IsValid() and box_2.GetSpecifier() == Sdf.SpecifierDef
        assert class_prim.IsValid() and class_prim.GetSpecifier() == Sdf.SpecifierClass
        assert nb.stage.GetDefaultPrim().GetPath() == "/World"
        assert (nb._work_dir / "_assets" / "specifiers_base.usda").exists()

    def test_cell_over_inherit(self, run_notebook):
        nb = run_notebook(
            SPECIFIERS_NOTEBOOK,
            tags=SPECIFIERS_SETUP + ["specifiers-def-and-class", "specifiers-over-inherit"],
        )
        assert nb.stage is not None
        box = nb.stage.GetPrimAtPath("/World/Box")
        assert box.IsValid()
        # Over prim composes with base; avoid querying untyped over-only attributes
        assert (nb._work_dir / "_assets" / "specifiers_over_base.usda").exists()


class TestReferencesNotebook:
    """Tests for composition-basics/references.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(REFERENCES_NOTEBOOK, needs_content=True)
        assert (nb._work_dir / "_assets" / "shapes.usda").exists()

    def test_cell_add_reference(self, run_notebook):
        nb = run_notebook(
            REFERENCES_NOTEBOOK,
            tags=REFERENCES_SETUP + ["references-add-reference"],
        )
        assert nb.stage is not None
        world = nb.stage.GetPrimAtPath("/World")
        sphere = nb.stage.GetPrimAtPath("/World/Sphere")
        cube_ref = nb.stage.GetPrimAtPath("/World/Cube_Ref")
        assert world.IsValid() and sphere.IsValid() and cube_ref.IsValid()
        assert cube_ref.HasAuthoredReferences()
        assert (nb._work_dir / "_assets" / "cube.usda").exists()
        assert (nb._work_dir / "_assets" / "shapes.usda").exists()

    def test_cell_external_asset(self, run_notebook):
        nb = run_notebook(
            REFERENCES_NOTEBOOK,
            tags=REFERENCES_SETUP + ["references-setup-asset", "references-external-asset"],
            needs_content=True,
        )
        assert nb.stage is not None
        box = nb.stage.GetPrimAtPath("/World/Geometry/Box")
        assert box.IsValid()
        assert box.HasAuthoredReferences()
        assert (nb._work_dir / "_assets" / "asset_ref.usda").exists()


class TestDefaultPrimNotebook:
    """Tests for composition-basics/default-prim.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(DEFAULT_PRIM_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "default_prim.usda").exists()

    def test_cell_default_prim_set(self, run_notebook):
        nb = run_notebook(
            DEFAULT_PRIM_NOTEBOOK,
            tags=DEFAULT_PRIM_SETUP + ["default-prim-set"],
        )
        assert nb.stage is not None
        assert "hello_prim" in nb
        assert nb.stage.GetDefaultPrim().GetPath() == "/hello"
        assert nb.stage.GetPrimAtPath("/hello").IsValid()
        assert nb.stage.GetPrimAtPath("/hello/world").IsValid()
        assert (nb._work_dir / "_assets" / "default_prim.usda").exists()
