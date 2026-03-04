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

"""Tests for beyond-basics doc notebooks (docs/beyond-basics/).

Notebooks are built to docs/_build/jupyter_execute/; paths are relative to that directory.
"""

import pytest


VALUE_RESOLUTION_NOTEBOOK = "beyond-basics/value-resolution.ipynb"
VALUE_RESOLUTION_SETUP = ["value-resolution-setup"]
VALUE_RESOLUTION_CELLS = [
    "value-resolution-setup",
    "value-resolution-attribute-animation",
    "value-resolution-customdata-relationship",
]

UNITS_NOTEBOOK = "beyond-basics/units.ipynb"
UNITS_SETUP = ["units-setup"]
UNITS_CELLS = [
    "units-setup",
    "units-meters-per-unit",
    "units-timecodes-per-second",
]

STAGE_TRAVERSAL_NOTEBOOK = "beyond-basics/stage-traversal.ipynb"
STAGE_TRAVERSAL_SETUP = ["stage-traversal-setup"]
STAGE_TRAVERSAL_CELLS = [
    "stage-traversal-setup",
    "stage-traversal-traverse",
    "stage-traversal-filter-types",
    "stage-traversal-children",
    "stage-traversal-prim-range",
]

PRIMVARS_NOTEBOOK = "beyond-basics/primvars.ipynb"
PRIMVARS_SETUP = ["primvars-setup"]
PRIMVARS_CELLS = [
    "primvars-setup",
    "primvars-displaycolor-interpolation",
    "primvars-mesh-deformation",
]

MODEL_KINDS_NOTEBOOK = "beyond-basics/model-kinds.ipynb"
MODEL_KINDS_SETUP = ["model-kinds-setup"]
MODEL_KINDS_CELLS = [
    "model-kinds-setup",
    "model-kinds-component-traversal",
]

CUSTOM_PROPERTIES_NOTEBOOK = "beyond-basics/custom-properties.ipynb"
CUSTOM_PROPERTIES_SETUP = ["custom-properties-setup", "custom-properties-setup-asset"]
CUSTOM_PROPERTIES_CELLS = [
    "custom-properties-setup",
    "custom-properties-setup-asset",
    "custom-properties-create-attributes",
    "custom-properties-modify-attributes",
    "custom-properties-namespaces",
]

ACTIVE_INACTIVE_NOTEBOOK = "beyond-basics/active-inactive-prims.ipynb"
ACTIVE_INACTIVE_SETUP = ["active-inactive-setup"]
ACTIVE_INACTIVE_CELLS = [
    "active-inactive-setup",
    "active-inactive-deactivate",
]


class TestValueResolutionNotebook:
    """Tests for beyond-basics/value-resolution.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(VALUE_RESOLUTION_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "value_resolution_composed_explicit.usda").exists()

    @pytest.mark.parametrize("cell_tag", VALUE_RESOLUTION_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = VALUE_RESOLUTION_SETUP + [cell_tag]
        nb = run_notebook(VALUE_RESOLUTION_NOTEBOOK, tags=tags)
        if cell_tag == "value-resolution-attribute-animation":
            assert "stage" in nb
        elif cell_tag == "value-resolution-customdata-relationship":
            assert "composed_stage" in nb or "xform_prim" in nb


class TestUnitsNotebook:
    """Tests for beyond-basics/units.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(UNITS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "units_timecode_scene.usda").exists()

    @pytest.mark.parametrize("cell_tag", UNITS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = list(UNITS_SETUP) + [cell_tag]
        nb = run_notebook(UNITS_NOTEBOOK, tags=tags)
        if cell_tag == "units-meters-per-unit":
            assert "scene_stage" in nb
        elif cell_tag == "units-timecodes-per-second":
            assert "scene_stage" in nb


class TestStageTraversalNotebook:
    """Tests for beyond-basics/stage-traversal.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(STAGE_TRAVERSAL_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "stage_traversal.usda").exists()

    @pytest.mark.parametrize("cell_tag", STAGE_TRAVERSAL_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = STAGE_TRAVERSAL_SETUP + [cell_tag]
        nb = run_notebook(STAGE_TRAVERSAL_NOTEBOOK, tags=tags)
        if cell_tag == "stage-traversal-traverse":
            assert "stage" in nb
        elif cell_tag == "stage-traversal-filter-types":
            assert "stage" in nb
        elif cell_tag == "stage-traversal-children":
            assert "stage" in nb
        elif cell_tag == "stage-traversal-prim-range":
            assert "stage" in nb


class TestPrimvarsNotebook:
    """Tests for beyond-basics/primvars.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(PRIMVARS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "primvars_mesh_deformation.usda").exists()

    @pytest.mark.parametrize("cell_tag", PRIMVARS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = PRIMVARS_SETUP + [cell_tag]
        nb = run_notebook(PRIMVARS_NOTEBOOK, tags=tags)
        if cell_tag in ("primvars-displaycolor-interpolation", "primvars-mesh-deformation"):
            assert "stage" in nb


class TestModelKindsNotebook:
    """Tests for beyond-basics/model-kinds.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(MODEL_KINDS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "model_kinds_component.usda").exists()

    @pytest.mark.parametrize("cell_tag", MODEL_KINDS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = MODEL_KINDS_SETUP + [cell_tag]
        nb = run_notebook(MODEL_KINDS_NOTEBOOK, tags=tags)
        if cell_tag == "model-kinds-component-traversal":
            assert "stage" in nb


class TestCustomPropertiesNotebook:
    """Tests for beyond-basics/custom-properties.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(CUSTOM_PROPERTIES_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "sensor_data.usda").exists()

    @pytest.mark.parametrize("cell_tag", CUSTOM_PROPERTIES_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = list(CUSTOM_PROPERTIES_SETUP) + [cell_tag]
        nb = run_notebook(CUSTOM_PROPERTIES_NOTEBOOK, tags=tags)
        if cell_tag == "custom-properties-create-attributes":
            assert "stage" in nb
        elif cell_tag == "custom-properties-modify-attributes":
            assert "stage" in nb
        elif cell_tag == "custom-properties-namespaces":
            assert "stage" in nb


class TestActiveInactivePrimsNotebook:
    """Tests for beyond-basics/active-inactive-prims.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(ACTIVE_INACTIVE_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "active-inactive.usda").exists()

    @pytest.mark.parametrize("cell_tag", ACTIVE_INACTIVE_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = ACTIVE_INACTIVE_SETUP + [cell_tag]
        nb = run_notebook(ACTIVE_INACTIVE_NOTEBOOK, tags=tags)
        if cell_tag == "active-inactive-deactivate":
            assert "stage" in nb
