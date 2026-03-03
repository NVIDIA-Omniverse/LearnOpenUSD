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

"""Pytest configuration and fixtures for notebook testing."""

import json
import os
from pathlib import Path

import pytest


class Notebook:
    """Attribute-accessible wrapper around a notebook execution namespace.
    
    Provides attribute access to variables from executed notebook cells
    and exposes the working directory where files were created.
    """
    
    def __init__(self, ns: dict, work_dir: Path):
        """Initialize the namespace wrapper.
        
        Args:
            ns: Dictionary of variables from notebook execution.
            work_dir: Path to the temporary working directory.
        """
        self.__dict__.update(ns)
        self._work_dir = work_dir
    
    def __contains__(self, key: str) -> bool:
        """Check if a variable exists in the namespace.
        
        Args:
            key: Variable name to check.
        
        Returns:
            True if the variable exists.
        """
        return key in self.__dict__


def _execute_notebook(
    notebook_path: str,
    cells: list[int] | None,
    tags: list[str] | None,
    work_dir: Path,
) -> Notebook:
    """Execute notebook cells and return the resulting namespace.
    
    Args:
        notebook_path: Path to notebook. If it starts with "tests/", resolved
            relative to repo root (for harness sanity notebooks). Otherwise
            relative to docs/_build/jupyter_execute/.
        cells: List of code cell indices to execute (0-indexed), or None for all cells.
        tags: List of test-tags to match; only cells with any of these tags run.
            Mutually exclusive with cells.
        work_dir: Temporary directory to use as working directory during execution.
    
    Returns:
        Notebook object with executed namespace.
    """
    if cells is not None and tags is not None:
        raise ValueError("Cannot specify both 'cells' and 'tags'")
    
    repo_root = Path(__file__).resolve().parent.parent
    if notebook_path.startswith("tests/"):
        nb_file = repo_root / notebook_path
    else:
        notebooks_base = repo_root / "docs" / "_build" / "jupyter_execute"
        nb_file = notebooks_base / notebook_path
    
    if not nb_file.exists():
        raise FileNotFoundError(f"Notebook not found: {nb_file}")
    
    # Load notebook
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)
    
    # Extract code cells
    code_cells = [cell for cell in nb_data.get('cells', []) if cell.get('cell_type') == 'code']
    
    # Determine which cells to execute (preserve document order)
    if tags is not None:
        requested_tags = set(tags)
        tags_in_notebook = set()
        for cell in code_cells:
            tags_in_notebook.update(cell.get('metadata', {}).get('test-tags', []))
        unmatched_tags = requested_tags - tags_in_notebook
        if unmatched_tags:
            raise ValueError(
                f"The following tags do not match any cell: {sorted(unmatched_tags)}. "
                f"Check for typos; valid tags in this notebook: {sorted(tags_in_notebook) or '(none)'}."
            )
        tag_set = requested_tags
        cells_to_run = [
            cell for cell in code_cells
            if tag_set & set(cell.get('metadata', {}).get('test-tags', []))
        ]
    elif cells is None:
        cells_to_run = code_cells
    else:
        n_code = len(code_cells)
        for i in cells:
            if i < 0 or i >= n_code:
                raise IndexError(
                    f"Code cell index {i} is out of range (notebook has {n_code} code cells, "
                    f"valid indices 0..{n_code - 1})"
                )
        cells_to_run = [code_cells[i] for i in cells]
    
    # Create _assets directory in work_dir
    assets_dir = work_dir / "_assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Execute cells in isolated namespace
    namespace = {}
    old_cwd = os.getcwd()
    try:
        os.chdir(work_dir)
        
        for cell in cells_to_run:
            source = cell.get('source', [])
            if isinstance(source, list):
                source = ''.join(source)
            
            # Execute the cell code
            exec(source, namespace)
    finally:
        os.chdir(old_cwd)
    
    return Notebook(namespace, work_dir)


@pytest.fixture
def run_notebook(tmp_path):
    """Pytest fixture factory for executing notebook cells.
    
    Returns a callable that takes a notebook path and optional cell indices
    or tags, executes the cells in an isolated environment, and returns a
    Notebook object with the resulting namespace.
    
    Args:
        tmp_path: Pytest's temporary directory fixture.
    
    Returns:
        Callable that executes notebooks and returns Notebook objects.
    
    Example:
        # Harness sanity (notebook under tests/):
        def test_harness(run_notebook):
            nb = run_notebook("tests/fixtures/harness_sanity.ipynb")
            assert nb.harness_sanity_ran is True

        # Lesson notebook (under docs/_build/jupyter_execute):
        def test_create_stage(run_notebook):
            nb = run_notebook("stage-setting/stage.ipynb", cells=[0])
            assert nb.stage is not None

        # By tag (cells run in document order):
        def test_setup_only(run_notebook):
            nb = run_notebook("stage-setting/stage.ipynb", tags=["setup"])
            assert nb.stage is not None
    """
    def _run(
        path: str,
        cells: list[int] | None = None,
        tags: list[str] | None = None,
    ) -> Notebook:
        return _execute_notebook(path, cells, tags, tmp_path)
    
    return _run
