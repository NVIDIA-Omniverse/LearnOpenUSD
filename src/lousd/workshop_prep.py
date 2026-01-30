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

"""Workshop preparation script for Learn OpenUSD.

This script transforms the full Learn OpenUSD documentation into a streamlined
workshop version by modifying the TOC, removing unused content, and converting
cross-references to external links.

The script performs the following steps:
    1. Updates the site title to reflect workshop branding
    2. Modifies the TOC to keep only workshop-relevant modules
    3. Removes unused module directories and files
    4. Removes setup pages from kept modules
    5. Converts cross-references to removed content into external links

Example:
    Run the script using uv::

        $ uv run workshop_prep
"""

import re
import shutil
from pathlib import Path

# Modules to keep in the main TOC
MODULES_TO_KEEP = [
    "creating-composition-arcs",
    "asset-structure",
    "data-exchange",
    "asset-modularity-instancing",
]

# Modules to remove entirely
MODULES_TO_REMOVE = [
    "what-openusd",
    "stage-setting",
    "scene-description-blueprints",
    "composition-basics",
    "beyond-basics",
]

# Individual files to remove
FILES_TO_REMOVE = [
    "usdview-install-instructions.md",
]

# Base URL for external links to removed content
EXTERNAL_BASE_URL = "https://docs.nvidia.com/learn-openusd/latest/"


def get_docs_dir() -> Path:
    """Get the docs directory path relative to this script.

    Returns:
        Path to the docs directory.
    """
    return Path(__file__).parent.parent.parent / "docs"


def modify_main_toc(docs_dir: Path) -> None:
    """Modify the main docs/index.md for the workshop.

    Rewrites the homepage to include only workshop-relevant content:
    - Keeps only the workshop modules in the main TOC
    - Keeps Common Resources with glossaries and Why Get Certified
    - Removes the Get Involved section
    - Adds module cards with Start Learning buttons

    Args:
        docs_dir: Path to the docs directory.
    """
    index_path = docs_dir / "index.md"
    
    # New simplified index.md content
    new_content = """
# Learn OpenUSD: Applied Concepts Workshop

In this workshop, students will develop a scalable and performant OpenUSD scene pipeline, from data ingestion and structuring to advanced composition and instancing, enabling efficient management of complex 3D environments. Students will learn to:
- Integrate and process external 3D data into OpenUSD.
- Structure assets effectively for improved collaboration, reuse, and pipeline efficiency.
- Compose complex 3D scenes using various OpenUSD composition arcs.
- Optimize scene performance and memory usage through advanced instancing techniques.

## Modules

::::::{grid} 2 2 2 2
:gutter: 3

:::::{grid-item-card} Creating Composition Arcs

Learn how to leverage composition arcs including sublayers, references, payloads, variant sets, inherits, and specializes to build flexible USD workflows.
+++
:::{button-ref} creating-composition-arcs/index
:color: primary
:expand:
Start Learning
:::
:::::

:::::{grid-item-card} Asset Structure Principles and Content Aggregation

Master the principles of asset organization, model hierarchy, workstreams, and the reference/payload pattern for production-ready assets.
+++
:::{button-ref} asset-structure/index
:color: primary
:expand:
Start Learning
:::
:::::

:::::{grid-item-card} DevelopingData Exchange Pipelines

Develop skills in data extraction, transformation, exchange, and validation for interoperability between USD and other formats.
+++
:::{button-ref} data-exchange/index
:color: primary
:expand:
Start Learning
:::
:::::

:::::{grid-item-card} Asset Modularity and Instancing

Explore scenegraph instancing and point instancing techniques to optimize scene performance and enable flexible asset reuse.
+++
:::{button-ref} asset-modularity-instancing/index
:color: primary
:expand:
Start Learning
:::
:::::

::::::

---

## Why Get Certified?

This learning path is designed to prepare you directly for the **OpenUSD Development Certification** exam—ensuring you gain real-world, in-demand skills and are ready for industry-recognized credentials.

**🎓 Learn more about [](why-openusd-developer-certification.md)**

---

:::{toctree}
:maxdepth: 2
:hidden:

Overview <self>
creating-composition-arcs/index
asset-structure/index
data-exchange/index
asset-modularity-instancing/index
:::

:::{toctree}
:caption: Common Resources
:maxdepth: 2
:hidden:

Glossary <glossary>
Interactive Glossary <interactive-glossary>
Why Get Certified <why-openusd-developer-certification>
:::
"""
    
    index_path.write_text(new_content, encoding="utf-8")
    print(f"Modified: {index_path}")


def update_site_title(docs_dir: Path) -> None:
    """Update the site title in conf.py to reflect workshop branding.

    Modifies the `project` variable in conf.py to set the title to
    "Learn OpenUSD: Applied Concepts Workshop".

    Args:
        docs_dir: Path to the docs directory.
    """
    conf_path = docs_dir / "conf.py"
    
    if not conf_path.exists():
        print(f"Warning: conf.py not found at {conf_path}")
        return
    
    content = conf_path.read_text(encoding="utf-8")
    
    # Update the project title
    new_content = re.sub(
        r"^project = ['\"].*['\"]",
        "project = 'Learn OpenUSD: Applied Concepts Workshop'",
        content,
        flags=re.MULTILINE
    )
    
    if new_content != content:
        conf_path.write_text(new_content, encoding="utf-8")
        print(f"Updated site title: {conf_path}")
    else:
        print(f"Site title already updated or pattern not found: {conf_path}")


def remove_unused_modules(docs_dir: Path) -> None:
    """Remove module directories and files not needed for the workshop.

    Deletes entire module directories listed in MODULES_TO_REMOVE and
    individual files listed in FILES_TO_REMOVE.

    Args:
        docs_dir: Path to the docs directory.
    """
    # Remove module directories
    for module in MODULES_TO_REMOVE:
        module_path = docs_dir / module
        if module_path.exists():
            shutil.rmtree(module_path)
            print(f"Removed directory: {module_path}")
    
    # Remove individual files
    for filename in FILES_TO_REMOVE:
        file_path = docs_dir / filename
        if file_path.exists():
            file_path.unlink()
            print(f"Removed file: {file_path}")


def remove_setup_pages(docs_dir: Path) -> None:
    """Remove setup.md files from kept modules and update their toctrees.

    For each module in MODULES_TO_KEEP, deletes the setup.md file if present
    and removes the "Setup <setup>" entry from the module's index.md toctree.

    Args:
        docs_dir: Path to the docs directory.
    """
    for module in MODULES_TO_KEEP:
        module_path = docs_dir / module
        setup_path = module_path / "setup.md"
        index_path = module_path / "index.md"
        
        # Remove setup.md if it exists
        if setup_path.exists():
            setup_path.unlink()
            print(f"Removed: {setup_path}")
        
        # Update the module's index.md to remove setup from toctree
        if index_path.exists():
            content = index_path.read_text(encoding="utf-8")
            # Remove "Setup <setup>" line from toctree
            content = re.sub(r'\nSetup <setup>\n', '\n', content)
            index_path.write_text(content, encoding="utf-8")
            print(f"Updated toctree: {index_path}")


def resolve_doc_reference_path(ref_path: str, current_file: Path, docs_dir: Path) -> str | None:
    """Resolve a reference path to determine if it points to removed content.

    Handles relative paths (../, ./), absolute paths (/), and paths relative
    to the current file's directory.

    Args:
        ref_path: The reference path from a {doc} directive or markdown link.
        current_file: Path to the file containing the reference.
        docs_dir: Path to the docs directory.

    Returns:
        The resolved path from docs root if it points to removed content,
        None otherwise.
    """
    # Handle relative paths
    if ref_path.startswith("../"):
        # Resolve relative to current file's directory
        current_dir = current_file.parent
        resolved = (current_dir / ref_path).resolve()
        try:
            rel_path = resolved.relative_to(docs_dir.resolve())
            path_str = str(rel_path).replace("\\", "/")
        except ValueError:
            return None
    elif ref_path.startswith("/"):
        # Absolute path from docs root
        path_str = ref_path.lstrip("/")
    else:
        # Relative to current directory
        current_dir = current_file.parent
        resolved = (current_dir / ref_path).resolve()
        try:
            rel_path = resolved.relative_to(docs_dir.resolve())
            path_str = str(rel_path).replace("\\", "/")
        except ValueError:
            return None
    
    # Check if it points to removed content
    for module in MODULES_TO_REMOVE:
        if path_str.startswith(module + "/") or path_str == module:
            return path_str
    
    # Check for removed individual files
    for filename in FILES_TO_REMOVE:
        base_name = filename.replace(".md", "")
        if path_str == base_name or path_str == filename:
            return base_name
    
    # Check for setup pages in kept modules
    for module in MODULES_TO_KEEP:
        if path_str == f"{module}/setup" or path_str == f"{module}/setup.md":
            return f"{module}/setup"
    
    return None


def convert_doc_reference(match: re.Match, current_file: Path, docs_dir: Path) -> str:
    """Convert a {doc} reference to an external link if it points to removed content.

    Handles both formats: {doc}`path` and {doc}`label <path>`.

    Args:
        match: Regex match object containing the {doc} reference.
        current_file: Path to the file containing the reference.
        docs_dir: Path to the docs directory.

    Returns:
        A markdown link to the external URL if the reference points to removed
        content, otherwise the original match string.
    """
    full_match = match.group(0)
    
    # Parse the {doc} reference - formats:
    # {doc}`path`
    # {doc}`label <path>`
    inner = match.group(1)
    
    # Check if it has a label
    label_match = re.match(r'(.+?)\s*<(.+?)>', inner)
    if label_match:
        label = label_match.group(1).strip()
        ref_path = label_match.group(2).strip()
    else:
        label = None
        ref_path = inner.strip()
    
    # Check if this points to removed content
    resolved_path = resolve_doc_reference_path(ref_path, current_file, docs_dir)
    
    if resolved_path:
        # Convert to external link
        # Ensure .html extension
        if not resolved_path.endswith(".html"):
            resolved_path = resolved_path.replace(".md", "") + ".html"
        
        external_url = EXTERNAL_BASE_URL + resolved_path
        display_label = label if label else ref_path.split("/")[-1].replace("-", " ").title()
        return f"[{display_label}]({external_url})"
    
    # Not removed content, keep original
    return full_match


def convert_markdown_link(match: re.Match, current_file: Path, docs_dir: Path) -> str:
    """Convert a markdown link to an external link if it points to removed content.

    Handles standard markdown links [text](path), including MyST angle bracket
    syntax [text](<path>). Preserves anchors and skips external links.

    Args:
        match: Regex match object containing the markdown link.
        current_file: Path to the file containing the link.
        docs_dir: Path to the docs directory.

    Returns:
        A markdown link to the external URL if the link points to removed
        content, otherwise the original match string.
    """
    full_match = match.group(0)
    label = match.group(1)
    link_path = match.group(2)
    
    # Strip angle brackets if present (MyST markdown syntax)
    if link_path.startswith("<") and link_path.endswith(">"):
        link_path = link_path[1:-1]
    
    # Skip external links
    if link_path.startswith("http://") or link_path.startswith("https://"):
        return full_match
    
    # Skip anchors-only links
    if link_path.startswith("#"):
        return full_match
    
    # Skip intersphinx references (inv: prefix)
    if link_path.startswith("inv:"):
        return full_match
    
    # Handle anchor in link
    anchor = ""
    if "#" in link_path:
        link_path, anchor = link_path.split("#", 1)
        anchor = "#" + anchor
    
    # Strip ./ prefix (relative to current directory/docs root)
    if link_path.startswith("./"):
        link_path = link_path[2:]
    
    # Resolve the path
    resolved_path = resolve_doc_reference_path(link_path, current_file, docs_dir)
    
    if resolved_path:
        # Convert to external link
        if not resolved_path.endswith(".html"):
            resolved_path = resolved_path.replace(".md", "") + ".html"
        
        external_url = EXTERNAL_BASE_URL + resolved_path + anchor
        return f"[{label}]({external_url})"
    
    # Not removed content, keep original
    return full_match


def convert_cross_references(docs_dir: Path) -> None:
    """Scan all .md files and convert references to removed content into external links.

    Processes all markdown files in the docs directory, converting {doc}
    references and standard markdown links that point to removed modules
    into external links using EXTERNAL_BASE_URL.

    Args:
        docs_dir: Path to the docs directory.
    """
    # Pattern for {doc} references
    doc_pattern = re.compile(r'\{doc\}`([^`]+)`')
    
    # Pattern for markdown links [text](path)
    md_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # Process all .md files in docs directory
    for md_file in docs_dir.rglob("*.md"):
        # Skip files in removed directories (they should be gone, but just in case)
        rel_path = md_file.relative_to(docs_dir)
        path_parts = rel_path.parts
        if path_parts and path_parts[0] in MODULES_TO_REMOVE:
            continue
        
        content = md_file.read_text(encoding="utf-8")
        original_content = content
        
        # Convert {doc} references
        content = doc_pattern.sub(
            lambda m: convert_doc_reference(m, md_file, docs_dir),
            content
        )
        
        # Convert markdown links
        content = md_link_pattern.sub(
            lambda m: convert_markdown_link(m, md_file, docs_dir),
            content
        )
        
        # Write back if changed
        if content != original_content:
            md_file.write_text(content, encoding="utf-8")
            print(f"Updated cross-references: {md_file}")


def main(docs_dir: Path | None = None) -> None:
    """Run the workshop preparation script.

    Executes all preparation steps in sequence: updates site title, modifies
    the TOC, removes unused modules, removes setup pages, and converts
    cross-references to external links.

    Args:
        docs_dir: Optional path to the docs directory. If None, uses get_docs_dir().
    """
    if docs_dir is None:
        docs_dir = get_docs_dir()
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return
    
    print("=" * 60)
    print("Workshop Preparation Script")
    print("=" * 60)
    print()
    
    print("Step 1: Updating site title...")
    update_site_title(docs_dir)
    print()
    
    print("Step 2: Modifying main TOC...")
    modify_main_toc(docs_dir)
    print()
    
    print("Step 3: Removing unused modules...")
    remove_unused_modules(docs_dir)
    print()
    
    print("Step 4: Removing setup pages...")
    remove_setup_pages(docs_dir)
    print()
    
    print("Step 5: Converting cross-references...")
    convert_cross_references(docs_dir)
    print()
    
    print("=" * 60)
    print("Workshop preparation complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Review the changes with: git diff")
    print("  2. Build the docs with: uv run sphinx-build -M html docs/ docs/_build/")
    print("  3. Preview locally with: uv run python -m http.server 8000 -d docs/_build/html/")

