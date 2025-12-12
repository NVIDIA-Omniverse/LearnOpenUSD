# Learn OpenUSD Style Guide

This style guide provides conventions for writing and formatting content in the Learn OpenUSD repository. Following these guidelines ensures consistency across all lessons and makes the content easier to read and maintain.

## Terminology and Spelling

### USD Terminology

All USD terminology should use the correct spelling as defined in the [OpenUSD Glossary](docs/glossary.md). Common terms include:

| Correct | Incorrect |
|---------|-----------|
| prim | Prim, PRIM |
| stage | Stage |
| layer | Layer |
| attribute | Attribute |
| relationship | Relationship |
| composition | Composition |
| reference | Reference |
| payload | Payload |
| variant set | VariantSet, Variant Set |
| sublayer | Sublayer, sub-layer |
| metadata | Metadata, meta-data |
| scenegraph | scene graph, SceneGraph |
| primvar | PrimVar, prim var |

### Capitalization Rules

- **USD terms should be lowercase** unless at the start of a sentence or in a title/heading.
- **Class and API names** should use their exact casing (e.g., `UsdGeom.Xform`, `Sdf.Layer`).
- **File extensions** should be lowercase (e.g., `.usda`, `.usd`, `.usdc`).

**Examples:**
- ✅ "A prim is the primary container in USD."
- ✅ "Prims can contain attributes and relationships."
- ❌ "A Prim is the primary container in USD."
- ✅ "The `UsdGeom.Xform` class defines transforms."

### Acronyms

- **USD** and **OpenUSD** are always capitalized.
- **LIVRPS** (strength ordering mnemonic) is always capitalized.
- Spell out acronyms on first use, then use the acronym: "Universal Scene Description (USD)"

## MyST Markdown Syntax

### Heading Structure

- Use `#` for the page title (appears once at the top)
- Use `##` for major sections
- Use `###` for subsections
- Use `####` sparingly for sub-subsections

### Glossary Terms

Link to glossary entries on first use in each lesson using the `{term}` role:

```markdown
OpenUSD {term}`stages <Stage>` are the foundation of scene composition.
```

The text before `<` is displayed; the text inside `<>` matches the glossary entry.

### Code Cells (Executable Python)

Use `{code-cell}` for Python code that executes during build:

````markdown
```{code-cell}
from pxr import Usd

stage = Usd.Stage.CreateNew("example.usda")
print(stage.ExportToString(addSourceFileComment=False))
```
````

**Code cell options:**

````markdown
```{code-cell}
:tags: [remove-input]
# This code runs but input is hidden from output
```

```{code-cell}
:emphasize-lines: 7-10
# Lines 7-10 will be highlighted
```
````

### Static Code Blocks

For non-executable code examples (API patterns, pseudocode):

````markdown
```python
# This code is displayed but not executed
stage.DefinePrim("/path", "Type")
```
````

### Videos

Embed Kaltura videos using the custom `{kaltura}` directive:

````markdown
```{kaltura} 1_cm4ehcvo
```
````

For local video files:

```markdown
![](../images/foundations/layer_Definition.webm)
```

### Admonitions

Use admonitions to highlight important information:

````markdown
```{seealso}
Read more about [USD File Formats](./usd-file-formats.md).
```

```{attention}
All exercises assume Visual Studio Code is open in the `usd_root/` directory.
```

```{caution}
Boolean operators like `and`/`or` will NOT combine predicates as intended.
```
````

Available admonition types: `note`, `warning`, `tip`, `caution`, `attention`, `seealso`, `important`

### Grid Layouts

Use grids for card-based layouts:

````markdown
::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Card Title
Card content here
:::

:::{grid-item-card} Another Card
More content
:::

::::
````

### Include Files

Include reusable content snippets:

````markdown
```{include} ../_includes/venv-table.md
```
````

### Cross-References

Link to other lessons using relative paths:

```markdown
See the [Sublayers lesson](../creating-composition-arcs/sublayers/index.md).
```

## Images and Media

### Image Placement

- Store images in `docs/images/<module-name>/`
- Use descriptive filenames: `layer_Definition.webm`, `strength-ordering-diagram.png`
- Supported formats: PNG, JPG, GIF, WEBM, MP4

### Image Syntax

With alt text (preferred for accessibility):

```markdown
![A diagram depicting independent layers building up to an aggregate scene.](../images/foundations/Layers.png)
```

Without alt text (for decorative images or videos):

```markdown
![](../images/foundations/layer_Definition.webm)
```

### Screenshots

- Capture only the relevant portion of the screen
- Use consistent window sizing when possible
- Avoid including or blur out personal information or unrelated UI elements

## Code Examples

### Python Code Style

- Follow PEP 8 style guidelines
- Use type hints for clarity: `stage: Usd.Stage = ...`
- Include imports in every code cell (cells should be self-contained)
- Use descriptive variable names

### Code Comments

- Add comments explaining each significant step
- Comments should explain "why" not just "what"
- Keep comments concise

**Example:**

```python
# Import the Usd module from the pxr package
from pxr import Usd

# Create a new stage at the specified path
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/example.usda")

# Define an Xform prim as the root of our scene
world = UsdGeom.Xform.Define(stage, "/World")

# Save changes to disk
stage.Save()
```

### Output

- Print meaningful output for learner verification
- Use `ExportToString(addSourceFileComment=False)` to avoid build-machine paths in output

### File Paths

- Save generated files to `_assets/` subdirectories to avoid committing them to the repo.
- Use relative paths from the lesson directory
- Use forward slashes even on Windows for consistency

## Writing Style

### Voice and Tone

- Use active voice: "We create a stage" not "A stage is created"
- Address the reader directly: "you will learn" not "learners will learn"
- Be concise but thorough
- Avoid jargon without explanation

### Technical Writing

- Use consistent terminology throughout
- Provide context for why something matters
- Include practical examples

### Transitions

- Connect sections with transitional sentences
- Preview what's coming: "In the next section, we will..."
- Summarize key points before moving on

## Exercise Files

### USD Files

- Store in `docs/exercise_content/<module-name>/`
- Use `.usda` for human-readable examples
- Use `.usd` for binary or format-agnostic files

### Python Scripts

- Include shebang and encoding if standalone
- Add docstrings explaining purpose
- Include license header


## Required File Headers

### License Header

Every new `.md` with executable code or `.py` file must include the Apache 2.0 SPDX license header:

```markdown
---
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
---
```

For Python files, use `#` comment syntax without the YAML delimiters.

### Jupytext Frontmatter

If the lesson includes executable Python code, add Jupytext metadata after the license header:

```markdown
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---
```

---

For questions about style not covered here, refer to existing lessons as examples or open an issue for clarification.

