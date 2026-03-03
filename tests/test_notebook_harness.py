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

"""Harness sanity checks for the notebook test infrastructure.

Uses a minimal fixture notebook (tests/fixtures/harness_sanity.ipynb) so these
tests are not affected by content changes in lesson notebooks like stage.ipynb.
"""

import os

import pytest


class TestNotebookHarness:
    """Sanity checks for the notebook execution harness (run_notebook fixture and Notebook wrapper)."""

    NOTEBOOK = "tests/fixtures/harness_sanity.ipynb"

    def test_full_notebook(self, run_notebook):
        """Run all code cells and verify the harness executes and exposes namespace."""
        nb = run_notebook(self.NOTEBOOK)

        assert nb.harness_sanity_ran is True
        assert nb.only_in_cell_1 is True
        assert nb.only_in_cell_2 is True
        assert "os" in nb
        assert nb.os is os
        assert nb.os.getcwd()

    def test_single_cell(self, run_notebook):
        """Run only code cell 0 and verify partial execution (cell numbering and import)."""
        nb = run_notebook(self.NOTEBOOK, cells=[0])

        assert nb.harness_sanity_ran is True
        assert nb.os is os
        assert nb.os.getcwd()
        assert "only_in_cell_1" not in nb
        assert "only_in_cell_2" not in nb

    def test_work_dir_and_file_creation(self, run_notebook):
        """Run all cells and verify work_dir is set and file was created under _assets."""
        nb = run_notebook(self.NOTEBOOK)

        sanity_file = nb._work_dir / "_assets" / "sanity_out.txt"
        assert sanity_file.exists()
        assert sanity_file.read_text() == "ok"

    def test_code_cell_1_only(self, run_notebook):
        """Run only code cell 1 (second code cell); verify index and no pollution from cell 0."""
        nb = run_notebook(self.NOTEBOOK, cells=[1])

        assert nb.only_in_cell_1 is True
        sanity_file = nb._work_dir / "_assets" / "sanity_out.txt"
        assert sanity_file.exists() and sanity_file.read_text() == "ok"
        assert "os" not in nb
        assert "harness_sanity_ran" not in nb
        assert "only_in_cell_2" not in nb

    def test_run_cells_0_and_2_no_pollution(self, run_notebook):
        """Run code cells 0 and 2 only; confirm cell 1 was not run (no pollution from unrun cell)."""
        nb = run_notebook(self.NOTEBOOK, cells=[0, 2])

        assert nb.harness_sanity_ran is True
        assert nb.only_in_cell_2 is True
        assert "os" in nb
        assert nb.os is os
        assert "only_in_cell_1" not in nb

    def test_single_tag(self, run_notebook):
        """Run only cells with tag 'setup'; verify partial execution."""
        nb = run_notebook(self.NOTEBOOK, tags=["setup"])

        assert nb.harness_sanity_ran is True
        assert nb.os is os
        assert nb.os.getcwd()
        assert "only_in_cell_1" not in nb
        assert "only_in_cell_2" not in nb

    def test_multiple_tags(self, run_notebook):
        """Run cells with tags 'setup' or 'final'; verify cells 0 and 2 run, cell 1 does not."""
        nb = run_notebook(self.NOTEBOOK, tags=["setup", "final"])

        assert nb.harness_sanity_ran is True
        assert nb.only_in_cell_2 is True
        assert "os" in nb
        assert nb.os is os
        assert "only_in_cell_1" not in nb

    def test_no_matching_tags_raises(self, run_notebook):
        """Run with a tag that no cell has; harness raises ValueError."""
        with pytest.raises(ValueError, match="The following tags do not match any cell"):
            run_notebook(self.NOTEBOOK, tags=["nonexistent"])

    def test_typo_in_tag_raises(self, run_notebook):
        """If any requested tag does not match a cell (e.g. typo), harness raises to avoid false positives."""
        with pytest.raises(ValueError, match="The following tags do not match any cell"):
            run_notebook(self.NOTEBOOK, tags=["setup", "finall"])  # typo: "finall"

    def test_cells_and_tags_exclusive(self, run_notebook):
        """Passing both cells and tags raises ValueError."""
        with pytest.raises(ValueError, match="Cannot specify both 'cells' and 'tags'"):
            run_notebook(self.NOTEBOOK, cells=[0], tags=["setup"])

    def test_cells_out_of_bounds_raises(self, run_notebook):
        """Passing a code cell index that is out of range raises IndexError."""
        with pytest.raises(IndexError, match="Code cell index .* out of range"):
            run_notebook(self.NOTEBOOK, cells=[0, 99])

    def test_cells_negative_index_raises(self, run_notebook):
        """Passing a negative code cell index raises IndexError."""
        with pytest.raises(IndexError, match="Code cell index .* out of range"):
            run_notebook(self.NOTEBOOK, cells=[-1])

    def test_tags_run_in_document_order(self, run_notebook):
        """Tagged cells run in document order, not in the order tags are passed."""
        # Request tags in reverse document order; cell 0 (setup) must still run before cell 2 (final)
        nb = run_notebook(self.NOTEBOOK, tags=["final", "setup"])

        assert nb.harness_sanity_ran is True  # set by cell 0
        assert nb.only_in_cell_2 is True  # set by cell 2; cell 0 ran first so namespace is shared
        assert nb.status == "finished" # final cell sets status to 'finished'
        assert "only_in_cell_1" not in nb
