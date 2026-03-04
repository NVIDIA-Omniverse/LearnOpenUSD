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
"""

import pytest


SPECIFIERS_NOTEBOOK = "composition-basics/specifiers.ipynb"
SPECIFIERS_SETUP = ["specifiers-setup"]
SPECIFIERS_CELLS = [
    "specifiers-setup",
    "specifiers-def-and-class",
    "specifiers-over-inherit",
]

REFERENCES_NOTEBOOK = "composition-basics/references.ipynb"
REFERENCES_SETUP = ["references-setup", "references-setup-asset"]
REFERENCES_CELLS = [
    "references-setup",
    "references-add-reference",
    "references-setup-asset",
    "references-external-asset",
]

DEFAULT_PRIM_NOTEBOOK = "composition-basics/default-prim.ipynb"
DEFAULT_PRIM_SETUP = ["default-prim-setup"]
DEFAULT_PRIM_CELLS = [
    "default-prim-setup",
    "default-prim-set",
]


class TestSpecifiersNotebook:
    """Tests for composition-basics/specifiers.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(SPECIFIERS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "specifiers_over_base.usda").exists()

    @pytest.mark.parametrize("cell_tag", SPECIFIERS_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = SPECIFIERS_SETUP + [cell_tag]
        nb = run_notebook(SPECIFIERS_NOTEBOOK, tags=tags)
        if cell_tag == "specifiers-def-and-class":
            assert "stage" in nb
        elif cell_tag == "specifiers-over-inherit":
            assert "stage" in nb


class TestReferencesNotebook:
    """Tests for composition-basics/references.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(REFERENCES_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "shapes.usda").exists()

    @pytest.mark.parametrize("cell_tag", REFERENCES_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        # references-external-asset needs asset copy (references-setup-asset)
        tags = list(REFERENCES_SETUP) + [cell_tag]
        nb = run_notebook(REFERENCES_NOTEBOOK, tags=tags)
        if cell_tag == "references-add-reference":
            assert "stage" in nb
        elif cell_tag == "references-external-asset":
            assert "stage" in nb


class TestDefaultPrimNotebook:
    """Tests for composition-basics/default-prim.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(DEFAULT_PRIM_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "default_prim.usda").exists()

    @pytest.mark.parametrize("cell_tag", DEFAULT_PRIM_CELLS)
    def test_cell(self, run_notebook, cell_tag):
        tags = DEFAULT_PRIM_SETUP + [cell_tag]
        nb = run_notebook(DEFAULT_PRIM_NOTEBOOK, tags=tags)
        if cell_tag == "default-prim-setting":
            assert "stage" in nb
            assert "hello_prim" in nb
