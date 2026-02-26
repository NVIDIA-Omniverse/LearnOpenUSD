# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "docs" / "_build" / "jupyter_execute"


def main() -> None:
    if not NOTEBOOKS_DIR.exists():
        print(f"Error: {NOTEBOOKS_DIR} not found.")
        print("Run the Sphinx build first: uv run sphinx-build -M html docs/ docs/_build/")
        sys.exit(1)

    print(f"==> Launching JupyterLab at {NOTEBOOKS_DIR}...")
    subprocess.run(
        [sys.executable, "-m", "jupyter", "lab", f"--notebook-dir={NOTEBOOKS_DIR}"],
        check=True,
    )

