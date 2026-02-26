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

"""Tests for the stage-setting/stage.ipynb notebook."""

from pathlib import Path


class TestStageNotebook:
    """Tests for the Stage lesson notebook."""

    NOTEBOOK = "stage-setting/stage.ipynb"

    def test_full_notebook(self, run_notebook):
        """Run all code cells and verify the notebook completes without error.
        
        This test executes all code cells in the stage notebook sequentially
        and verifies that key variables exist in the final namespace.
        """
        nb = run_notebook(self.NOTEBOOK)
        
        # Verify all key objects from the notebook exist
        assert "stage" in nb
        assert "root_layer" in nb
        assert "extra_layer" in nb
        
        # Verify the final stage has expected content
        assert nb.root_layer is not None
        assert nb.extra_layer is not None

    def test_create_new_stage(self, run_notebook):
        """Run only the first code cell (CreateNew) and check stage creation.
        
        This test verifies that the first example (creating a new USD stage)
        works correctly and produces the expected file and stage object.
        """
        nb = run_notebook(self.NOTEBOOK, cells=[0])
        
        # Verify the expected variables exist
        assert "stage" in nb
        assert "file_path" in nb
        
        # Check the file path is correct
        assert nb.file_path == "_assets/first_stage.usda"
        
        # Check the stage was created
        assert nb.stage is not None
        
        # Verify the file was created on disk
        stage_file = nb._work_dir / "_assets" / "first_stage.usda"
        assert stage_file.exists()

    def test_create_and_open_stage(self, run_notebook):
        """Run cells 0-1 (CreateNew + Open/Save) and verify the prim was added.
        
        This test runs the first two code cells sequentially:
        1. Create a new empty stage
        2. Open it, add a prim, and save
        
        It verifies that the second cell successfully opened the file from
        the first cell and added the expected prim to the stage.
        """
        nb = run_notebook(self.NOTEBOOK, cells=[0, 1])
        
        # Verify both cells executed
        assert "stage" in nb
        
        # Check that the /World prim was added in cell 1
        prim = nb.stage.GetPrimAtPath("/World")
        assert prim.IsValid()
        
        # Verify it's an Xform
        assert prim.GetTypeName() == "Xform"
