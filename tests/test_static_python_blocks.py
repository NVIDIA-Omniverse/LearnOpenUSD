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

"""Check static Python examples for syntax errors without executing fragments."""

import ast
import subprocess
import textwrap
from pathlib import Path

import pytest
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]


def python_blocks():
    parser = MarkdownIt("commonmark")
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "docs/*.md"], cwd=ROOT
    ).decode().split("\0")
    for relative in sorted(filter(None, paths)):
        for token in parser.parse((ROOT / relative).read_text(encoding="utf-8")):
            if token.type == "fence" and token.info.strip() == "python":
                line = token.map[0] + 1
                yield pytest.param(token.content, relative, line, id=f"{relative}:{line}")


@pytest.mark.parametrize("source,path,line", list(python_blocks()))
def test_static_python_syntax(source, path, line):
    ast.parse(textwrap.dedent(source), filename=f"{path}:{line}")
