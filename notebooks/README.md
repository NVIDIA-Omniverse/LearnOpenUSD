# Learn OpenUSD — Runnable Notebooks

Nine companion Jupyter notebooks that mirror every module of the
[Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/) curriculum and
convert it into executable cells you can run, edit, and experiment with.

The canonical source for each lesson lives under `../docs/`. These notebooks
replicate the same examples in a single, self-contained file per module, with
inline USDA previews and defensive fallbacks so every cell runs clean against a
bare `usd-core` install.

## Setup

From the repo root:

```bash
uv sync                      # installs usd-core, jupyterlab, the lousd helpers, etc.
git lfs install && git lfs pull   # exercise USD files are stored with Git LFS
uv run jupyter lab notebooks/
```

If you don't use `uv`, a minimal alternative is:

```bash
pip install usd-core jupyterlab
jupyter lab notebooks/
```

Without the `lousd` package installed, each notebook's third cell falls back to
inline helpers that print USDA text instead of the rich 3D `DisplayUSD` viewer —
everything still runs, you just lose the embedded WebGL preview.

## Recommended reading order

| #  | Notebook                                      | Covers                                                         |
| -- | --------------------------------------------- | -------------------------------------------------------------- |
| 00 | `00_what_is_openusd.ipynb`                    | What OpenUSD is and why industries adopt it                    |
| 01 | `01_stage_setting.ipynb`                      | Stages, prims, attributes, relationships, time codes, paths, file formats, modules, metadata |
| 02 | `02_scene_description_blueprints.ipynb`       | Schemas, Scope, Xform, XformCommonAPI, lights                  |
| 03 | `03_composition_basics.ipynb`                 | Layers, strength ordering, specifiers, references, default prim, variant sets |
| 04 | `04_beyond_basics.ipynb`                      | Primvars, value resolution, custom properties, active/inactive prims, model kinds, stage traversal, Hydra, units |
| 05 | `05_creating_composition_arcs.ipynb`          | Sublayers, references/payloads, variant sets, encapsulation, inherits/specializes, LIVRPS |
| 06 | `06_asset_structure.ipynb`                    | Asset interface, workstreams, parameterization, reference/payload pattern, model hierarchy |
| 07 | `07_asset_modularity_instancing.ipynb`        | Modularity, scenegraph instancing (authoring + refinement), point instancing |
| 08 | `08_data_exchange.ipynb`                      | Data exchange, extraction, transformation, asset validation    |

Start at `00` if you're new to OpenUSD, or jump straight to the module you need.

## How the notebooks are structured

Every notebook follows the same four-cell opening:

1. Title + learning objectives (markdown).
2. **Environment check** — prints Python version, confirms `pxr` imports, creates `./_assets/`.
3. **Helper bootstrap** — imports `create_new_stage` and `DisplayUSD` from the repo's `lousd` package, with inline fallbacks if it isn't installed.
4. (Modules 03+) **Exercise content staging** — walks up from the notebook directory to find `docs/exercise_content/`, copies shared USD files into `./_assets/`, and sets a `HAVE_*` flag so downstream cells skip gracefully if the content is missing.

After that, each lesson is one or more `## N.M  Lesson Title` sections
containing a concept summary, runnable code cells (with the original `test-tags`
from the source `.md` preserved as Jupyter cell tags), an inline preview cell,
and a short "what just happened" note.

## `_assets/` directory

Every code cell writes into `./_assets/` relative to the notebook. That folder
is gitignored and safe to delete any time — the notebooks recreate everything
they need on the next run.

## Relationship to the docs site

These notebooks do not replace the published site — the
[Learn OpenUSD docs](https://docs.nvidia.com/learn-openusd/latest/) include
videos, diagrams, and prose that aren't reproduced here. Use the notebooks for
hands-on experimentation and the site for conceptual depth. To build the full
site locally:

```bash
uv run sphinx-build -M html docs/ docs/_build/
uv run python -m http.server 8000 -d docs/_build/html/
```
