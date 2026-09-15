---
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
# List Editing

You have already used {term}`list editing <List Editing>` without being told what it was. Every time a lesson authored `prepend references = ...`, that `prepend` was a list-editing operation, and there are four more.

## What Is List Editing?

Most {term}`metadata <Metadata>` in OpenUSD resolves by strength: the strongest {term}`opinion <Direct Opinion>` wins and the rest are ignored. Ordered lists do not work that way. If they did, a shot {term}`layer <Layer>` adding one {term}`reference <Reference>` would wipe out every reference the asset layer had contributed.

Instead, list-valued fields **compose**. Each layer contributes operations — add this to the front, remove that one — and OpenUSD combines them from weakest to strongest into a final list.

Many fields are list-edited, and they all share the same machinery:

- Composition arcs: `references`, `payload`, `inherits`, `specializes`, `variantSets`
- `apiSchemas`, the list of applied {term}`API schemas <API Schema>`
- {term}`Relationship <Relationship>` targets and {term}`attribute <Attribute>` connections

```{important}
`subLayers` is **not** list-edited, despite looking like it should be. See [subLayers Is the Exception](#sublayers-is-the-exception) below — this trips people up regularly.
```

The examples in this lesson use relationship targets, because `GetTargets()` returns the composed list in one call and makes the mechanism easy to see. Everything shown applies identically to references, inherits, and the rest.

## The Operations

| Operation | `.usda` syntax | Effect |
| --- | --- | --- |
| Prepend | `prepend rel members = ...` | Add to the front of the composed list |
| Append | `append rel members = ...` | Add to the back |
| Delete | `delete rel members = ...` | Remove a matching item contributed by a weaker layer |
| Reorder | `reorder rel members = ...` | Constrain relative order without adding or removing |
| Reset to explicit | `rel members = [...]` (no keyword) | Discard everything weaker and use exactly this list |

There is also a legacy `add` operation that still parses but should not be used in new content.

### Prepend and Append Make a Sandwich

A stronger layer's `prepend` lands in front of *everything* the weaker layers contributed, and its `append` lands behind *everything* they contributed. The weaker layer's items end up in the middle.

```{caution}
This has a consequence worth pausing on: for composition arcs, **list order is strength order** — the first arc is the strongest. So `append` from a strong layer produces the *weakest* arc on that prim. A strong layer can author a weak opinion, and that is a very common source of "why isn't my reference winning?"
```

### Delete Only Reaches Downward

`delete` removes an item contributed by a **weaker** layer. It never reaches upward: if a stronger layer prepends the same item back, the item is present.

Matching is on the whole value, not on a string. For a reference, that means the asset path *and* prim path *and* layer offset all have to match. The asset path is anchored to the layer that authored it before comparison, so `@./B.usda@` in one layer and `@../B.usda@` in a layer one directory down do match if they resolve to the same file. A delete whose layer offset differs will silently fail to match.

### Reset to Explicit Is a Reset, Not a Lock

Authoring the bare form with no keyword discards every weaker opinion. It is the "stop listening to the layers below me" escape hatch.

It only blocks *weaker* layers, though. An explicit list is still freely edited by `prepend`, `append`, and `delete` in **stronger** layers. Explicit is not a lock.

```{note}
An explicit *empty* list serializes as `references = None`, not `references = []`. Both spellings parse identically, but OpenUSD always writes the `None` form, so a hand-typed `[]` round-trips into `None`.
```

### Reorder Is the One That Surprises People

`reorder` never adds and never removes — it only permutes items already in the composed list. Names that are not in the list are silently ignored, with no warning.

The part that catches people out is what "reorder" actually guarantees. It is **not** "move these to the front." It is a *relative-order constraint*: OpenUSD rearranges only as much as needed to make the named items appear in the order given, and unnamed neighbors get dragged along.

On a base list of `[A, B, C, D]`:

| Reorder | Result | Why |
| --- | --- | --- |
| `[C, A]` | `[C, D, A, B]` | `C` before `A`; `D` came forward with `C` |
| `[C, B]` | `[A, C, D, B]` | `C` before `B`; `B` pushed to the back |
| `[B, D]` | `[A, B, C, D]` | **No-op** — `B` was already before `D` |

Reorders from several layers accumulate weakest to strongest rather than replacing one another, and a reorder cannot resurrect a deleted item.

## Working With Python

Position is controlled by {usdcpp}`UsdListPosition`, which has exactly four values, reachable only as module-level names:

```python
Usd.ListPositionFrontOfPrependList
Usd.ListPositionBackOfPrependList   # the default
Usd.ListPositionFrontOfAppendList
Usd.ListPositionBackOfAppendList
```

```{caution}
`AddReference` defaults to `BackOfPrependList`, so it authors **`prepend`**, not `append`, despite being named "Add".

For references and payloads the argument after the paths is `layerOffset`, *not* position — `AddReference(path, primPath, Usd.ListPositionBackOfAppendList)` raises an error. Always pass position as a keyword: `position=Usd.ListPositionBackOfAppendList`.
```

There are three different ways to "remove" something, and they are not interchangeable:

| Call | What it authors | Effect on weaker layers |
| --- | --- | --- |
| `ClearReferences()` | nothing (erases only this layer's opinion) | weaker references **come back** |
| `RemoveReference(...)` | `delete references = ...` | weaker reference is **blocked** |
| `SetReferences([])` | `references = None` | **everything** weaker is blocked |

Reaching for `Clear` when you meant to block is a real bug, and it fails quietly.

Two more API facts worth knowing. `SetReferences()` with a non-empty list authors an *explicit* list op, so it is not a convenience wrapper around repeated `AddReference` calls — it blocks weaker layers. And `Usd.References` has no getter at all; to read back what a layer authored you go through `prim.GetMetadata("references")`, which returns an `Sdf.ReferenceListOp`.

```{note}
There is no convenience API for `reorder`. To author one you hand a raw list op with `orderedItems` set to either `Usd.Prim.SetMetadata()` or an `Sdf` spec's list editor, such as `spec.targetPathList.orderedItems = [...]`.
```

## Examples

```{tip}
You can run these examples locally as Jupyter notebooks. See [How to Run Notebooks Locally](../jupyter-notebook-setup.md) for setup instructions.
```

+++ {"tags": ["remove-cell"]}
>**NOTE**: Before starting make sure to run the cell below. This will install the relevant OpenUSD libraries that will be used through this notebook.
+++
```{code-cell}
:tags: [remove-input]
:test-tags: [list-editing-setup]
from pxr import Usd, Sdf


def build_stack():
    """Return a stage whose root has two sublayers: strong, then weak."""
    weak = Sdf.Layer.CreateAnonymous("weak.usda")
    strong = Sdf.Layer.CreateAnonymous("strong.usda")
    root = Sdf.Layer.CreateAnonymous("root.usda")
    # The first sublayer is the strongest
    root.subLayerPaths[:] = [strong.identifier, weak.identifier]
    return Usd.Stage.Open(root), weak, strong


def members(stage):
    """Create or fetch the relationship the examples edit."""
    return stage.DefinePrim("/World/Set").CreateRelationship("members")


def composed(stage):
    return [str(p) for p in stage.GetPrimAtPath("/World/Set").GetRelationship("members").GetTargets()]
```

### Example 1: Prepend and Append Across Layers

The weak layer contributes `A`, `B`, `C`. The strong layer prepends `D` and appends `E`. Watch where they land.

```{code-cell}
:test-tags: [list-editing-sandwich]
:emphasize-lines: 9-12

from pxr import Usd

stage, weak, strong = build_stack()

with Usd.EditContext(stage, weak):
    for path in ["/A", "/B", "/C"]:
        members(stage).AddTarget(path)

with Usd.EditContext(stage, strong):
    # BackOfPrependList is the default, shown here for clarity
    members(stage).AddTarget("/D", Usd.ListPositionBackOfPrependList)
    members(stage).AddTarget("/E", Usd.ListPositionBackOfAppendList)

print("what the strong layer authored:")
print(strong.ExportToString())
print("composed:", composed(stage))
```

The strong layer's `prepend` went in front of all three weaker items and its `append` went behind all three, producing `['/D', '/A', '/B', '/C', '/E']`. If these were references, `/E` would be the weakest arc on the prim despite being authored in the strongest layer.

### Example 2: The Three Ways to Remove

Here the same weak layer is combined with three different strong-layer edits, to show that `delete`, reset-to-explicit, and clear are three genuinely different operations.

```{code-cell}
:test-tags: [list-editing-removal]
:emphasize-lines: 10-11, 17-18, 24-25

from pxr import Usd

def weak_abc(stage, weak):
    with Usd.EditContext(stage, weak):
        for path in ["/A", "/B", "/C"]:
            members(stage).AddTarget(path)

# 1. delete: removes one item contributed by the weaker layer
stage, weak, strong = build_stack()
weak_abc(stage, weak)
with Usd.EditContext(stage, strong):
    members(stage).RemoveTarget("/B")
print("RemoveTarget('/B') ->", composed(stage))
removal_delete = composed(stage)

# 2. reset to explicit: discards everything weaker
stage, weak, strong = build_stack()
weak_abc(stage, weak)
with Usd.EditContext(stage, strong):
    members(stage).SetTargets(["/X", "/Y"])
print("SetTargets(['/X','/Y']) ->", composed(stage))
removal_explicit = composed(stage)

# 3. clear: erases only this layer's own opinion
stage, weak, strong = build_stack()
weak_abc(stage, weak)
with Usd.EditContext(stage, strong):
    members(stage).ClearTargets(removeSpec=False)
print("ClearTargets() ->", composed(stage))
removal_clear = composed(stage)
```

`RemoveTarget` authored a `delete` and took `/B` out. `SetTargets` reset the list to exactly what it was given, discarding the weak layer entirely. `ClearTargets` removed the strong layer's own opinion, so the weak layer shows through unchanged — which is the behavior people expect from the other two.

### Example 3: Reorder Is Not Move-to-Front

Three reorders against the same base list of `[A, B, C, D]`.

```{code-cell}
:test-tags: [list-editing-reorder]
:emphasize-lines: 13-14

from pxr import Usd, Sdf

reorder_results = {}

for order in (["/C", "/A"], ["/C", "/B"], ["/B", "/D"]):
    stage, weak, strong = build_stack()
    with Usd.EditContext(stage, weak):
        for path in ["/A", "/B", "/C", "/D"]:
            members(stage).AddTarget(path)

    # There is no Usd-level API for reorder, so author it through the Sdf spec
    with Usd.EditContext(stage, strong):
        members(stage)
    strong.GetRelationshipAtPath("/World/Set.members").targetPathList.orderedItems = order

    reorder_results[tuple(order)] = composed(stage)
    print(f"reorder {order} -> {composed(stage)}")
```

Only the *relative* order of the named items is guaranteed. `reorder ['/C', '/A']` dragged `/D` forward along with `/C`, and `reorder ['/B', '/D']` did nothing at all because `/B` already preceded `/D`.

(#sublayers-is-the-exception)=
## subLayers Is the Exception

`subLayers` looks like it should be list-edited and is not. Its field type is a plain vector of strings, not a list op, and the list-op keywords are **hard parse errors** on it — a file containing `prepend subLayers = [...]` fails to open rather than being quietly ignored.

The practical consequence is the important part:

> A stronger layer **can** delete a reference contributed by a weaker layer. It **cannot** delete a sublayer contributed by a weaker layer, because `delete subLayers` is not valid syntax.

Sublayer composition is governed by each layer's own flat list, resolved recursively. If a weaker layer brings in a sublayer you do not want, your options are to edit the layer that actually owns that entry, or to mute it — see [Edit Targets and Layer Muting](./edit-targets-layer-muting.md). Muting is stage state and cannot be shipped in a file the way a `delete references` can.

```{note}
`layer.subLayerPaths` behaves like a Python list but is not one: `remove()` on a missing item is a **silent no-op** rather than a `ValueError`, and `index()` returns `-1` instead of raising. A typo in a sublayer path therefore fails quietly.
```

## Key Takeaways

List editing is why a shot layer can add one reference without destroying the ones an asset layer contributed. Lists compose from weakest to strongest out of five operations: `prepend`, `append`, `delete`, `reorder`, and reset-to-explicit.

Three things are worth remembering past this lesson. Because list order is strength order for composition arcs, **`append` from a strong layer produces a weak arc** — if an arc is not winning, check which end of the list it landed on. **`reorder` is a relative-order constraint, not move-to-front**, and it is a no-op when the requested order already holds. And **`Clear`, `Remove`, and `Set([])` are three different removals**: only the last two block a weaker layer, and choosing the wrong one fails silently.

Finally, `subLayers` is not list-edited at all. When you need to suppress a sublayer, reach for muting or edit the owning layer.
