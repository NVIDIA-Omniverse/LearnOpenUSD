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

"""Tests for stage-setting doc notebooks (docs/stage-setting/).

Notebooks are built to docs/_build/jupyter_execute/; paths are relative to that directory.
Each class targets one notebook with a full-notebook test and per-cell tests (setup + cell).
"""

import pytest


# Notebook path and tag configuration. Setup tags must run before dependent cells.
STAGE_NOTEBOOK = "stage-setting/stage.ipynb"
STAGE_SETUP = []
STAGE_CELLS = [
    "stage-create-new",
    "stage-open-save",
    "stage-create-in-memory",
    "stage-root-layer",
]

PRIMS_NOTEBOOK = "stage-setting/prims.ipynb"
PRIMS_SETUP = ["prims-setup"]
PRIMS_CELLS = [
    "prims-setup",
    "prims-define-prim",
    "prims-sphere",
    "prims-hierarchy",
    "prims-getchild-box",
    "prims-getchild-group-transform",
]

PATHS_NOTEBOOK = "stage-setting/prim-property-paths.ipynb"
PATHS_SETUP = ["paths-setup"]
PATHS_CELLS = [
    "paths-setup",
    "paths-get-validate-define",
    "paths-build-and-navigate",
    "paths-property-authoring",
]

TIMECODES_NOTEBOOK = "stage-setting/timecodes-timesamples.ipynb"
TIMECODES_SETUP = ["timecodes-setup"]
TIMECODES_CELLS = [
    "timecodes-setup",
    "timecodes-sample-stage",
    "timecodes-set-start-end",
    "timecodes-translation-time-samples",
    "timecodes-scale-time-samples",
]

RELATIONSHIPS_NOTEBOOK = "stage-setting/properties/relationships.ipynb"
RELATIONSHIPS_SETUP = ["relationships-setup"]
RELATIONSHIPS_CELLS = [
    "relationships-setup",
    "relationships-prim-collections",
    "relationships-proxy-prim",
    "relationships-material-binding",
]

ATTRIBUTES_NOTEBOOK = "stage-setting/properties/attributes.ipynb"
ATTRIBUTES_SETUP = ["attributes-setup"]
ATTRIBUTES_CELLS = [
    "attributes-setup",
    "attributes-retrieve-properties",
    "attributes-get-values",
    "attributes-set-values",
]


class TestStageNotebook:
    """Tests for stage-setting/stage.ipynb (no setup cells)."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(STAGE_NOTEBOOK)
        assert "stage" in nb
        assert nb.stage is not None

    @pytest.mark.parametrize("cell_tag", STAGE_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = STAGE_SETUP + [cell_tag]
        nb = run_notebook(STAGE_NOTEBOOK, tags=tags)
        if cell_tag == "stage-create-new":
            assert nb.stage is not None
        elif cell_tag == "stage-open-save":
            assert nb.stage is not None
        elif cell_tag == "stage-create-in-memory":
            assert nb.stage is not None
        elif cell_tag == "stage-root-layer":
            assert nb.stage is not None
            assert "root_layer" in nb


class TestPrimsNotebook:
    """Tests for stage-setting/prims.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(PRIMS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "prim_hierarchy.usda").exists()

    @pytest.mark.parametrize("cell_tag", PRIMS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = PRIMS_SETUP + [cell_tag]
        nb = run_notebook(PRIMS_NOTEBOOK, tags=tags)
        if cell_tag == "prims-define-prim":
            assert "stage" in nb
        elif cell_tag == "prims-sphere":
            assert "stage" in nb
        elif cell_tag == "prims-hierarchy":
            assert "stage" in nb
        elif cell_tag == "prims-getchild-box":
            assert "stage" in nb
        elif cell_tag == "prims-getchild-group-transform":
            assert "stage" in nb


class TestPrimPropertyPathsNotebook:
    """Tests for stage-setting/prim-property-paths.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(PATHS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "paths_property_authoring.usda").exists()

    @pytest.mark.parametrize("cell_tag", PATHS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = PATHS_SETUP + [cell_tag]
        nb = run_notebook(PATHS_NOTEBOOK, tags=tags)
        if cell_tag == "paths-get-validate-define":
            assert "stage" in nb
        elif cell_tag == "paths-build-and-navigate":
            assert "stage" in nb
        elif cell_tag == "paths-property-authoring":
            assert "stage" in nb


class TestTimecodesTimesamplesNotebook:
    """Tests for stage-setting/timecodes-timesamples.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(TIMECODES_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "timecode_ex2b.usda").exists()

    @pytest.mark.parametrize("cell_tag", TIMECODES_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = TIMECODES_SETUP + [cell_tag]
        nb = run_notebook(TIMECODES_NOTEBOOK, tags=tags)
        if cell_tag == "timecodes-sample-stage":
            assert "stage" in nb
        elif cell_tag == "timecodes-set-start-end":
            assert "stage" in nb
        elif cell_tag == "timecodes-translation-samples":
            assert "stage" in nb
        elif cell_tag == "timecodes-scale-samples":
            assert "stage" in nb


class TestRelationshipsNotebook:
    """Tests for stage-setting/properties/relationships.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(RELATIONSHIPS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "relationships_ex3.usda").exists()

    @pytest.mark.parametrize("cell_tag", RELATIONSHIPS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = RELATIONSHIPS_SETUP + [cell_tag]
        nb = run_notebook(RELATIONSHIPS_NOTEBOOK, tags=tags)
        if cell_tag == "relationships-prim-collections":
            assert "stage" in nb
        elif cell_tag == "relationships-proxy-prim":
            assert "stage" in nb
        elif cell_tag == "relationships-material-binding":
            assert "stage" in nb


class TestAttributesNotebook:
    """Tests for stage-setting/properties/attributes.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(ATTRIBUTES_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "attributes_ex3.usda").exists()

    @pytest.mark.parametrize("cell_tag", ATTRIBUTES_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = ATTRIBUTES_SETUP + [cell_tag]
        nb = run_notebook(ATTRIBUTES_NOTEBOOK, tags=tags)
        if cell_tag == "attributes-retrieve-properties":
            assert "stage" in nb
        elif cell_tag == "attributes-get-values":
            assert "stage" in nb
        elif cell_tag == "attributes-set-values":
            assert "stage" in nb
