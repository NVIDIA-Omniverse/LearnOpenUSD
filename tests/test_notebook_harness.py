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
