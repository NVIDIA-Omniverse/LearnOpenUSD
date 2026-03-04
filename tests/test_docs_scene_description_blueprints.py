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
"""

import pytest


XFORM_NOTEBOOK = "scene-description-blueprints/xform.ipynb"
XFORM_SETUP = []
XFORM_CELLS = ["xform-define-world"]

SCOPE_NOTEBOOK = "scene-description-blueprints/scope.ipynb"
SCOPE_SETUP = ["scope-setup"]
SCOPE_CELLS = ["scope-setup", "scope-define-scopes"]

XFORMCOMMONAPI_NOTEBOOK = "scene-description-blueprints/xformcommonapi.ipynb"
XFORMCOMMONAPI_SETUP = ["xformcommonapi-setup"]
XFORMCOMMONAPI_CELLS = [
    "xformcommonapi-setup",
    "xformcommonapi-transforms-inheritance",
]

MATERIALS_NOTEBOOK = "scene-description-blueprints/materials-shaders.ipynb"
MATERIALS_SETUP = ["materials-setup"]
MATERIALS_CELLS = ["materials-setup", "materials-usdshade-material"]

LIGHTS_NOTEBOOK = "scene-description-blueprints/lights.ipynb"
LIGHTS_SETUP = ["lights-setup"]
LIGHTS_CELLS = [
    "lights-setup",
    "lights-distant-light",
    "lights-properties",
]


class TestXformNotebook:
    """Tests for scene-description-blueprints/xform.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(XFORM_NOTEBOOK)
        assert nb.stage is not None

    @pytest.mark.parametrize("cell_tag", XFORM_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = XFORM_SETUP + [cell_tag]
        nb = run_notebook(XFORM_NOTEBOOK, tags=tags)
        assert nb.stage is not None


class TestScopeNotebook:
    """Tests for scene-description-blueprints/scope.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(SCOPE_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "scope.usda").exists()

    @pytest.mark.parametrize("cell_tag", SCOPE_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = SCOPE_SETUP + [cell_tag]
        nb = run_notebook(SCOPE_NOTEBOOK, tags=tags)
        if cell_tag == "scope-define-scopes":
            assert "stage" in nb


class TestXformcommonapiNotebook:
    """Tests for scene-description-blueprints/xformcommonapi.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(XFORMCOMMONAPI_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "xformcommonapi.usda").exists()

    @pytest.mark.parametrize("cell_tag", XFORMCOMMONAPI_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = XFORMCOMMONAPI_SETUP + [cell_tag]
        nb = run_notebook(XFORMCOMMONAPI_NOTEBOOK, tags=tags)
        if cell_tag == "xformcommonapi-transforms-inheritance":
            assert "stage" in nb


class TestMaterialsShadersNotebook:
    """Tests for scene-description-blueprints/materials-shaders.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(MATERIALS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "materials.usda").exists()

    @pytest.mark.parametrize("cell_tag", MATERIALS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = MATERIALS_SETUP + [cell_tag]
        nb = run_notebook(MATERIALS_NOTEBOOK, tags=tags)
        if cell_tag == "materials-usdshade-material":
            assert "stage" in nb


class TestLightsNotebook:
    """Tests for scene-description-blueprints/lights.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(LIGHTS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "light_props.usda").exists()

    @pytest.mark.parametrize("cell_tag", LIGHTS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = LIGHTS_SETUP + [cell_tag]
        nb = run_notebook(LIGHTS_NOTEBOOK, tags=tags)
        if cell_tag == "lights-distant-light":
            assert "stage" in nb
        elif cell_tag == "lights-properties":
            assert "stage" in nb
