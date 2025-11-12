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
# Variant Sets Basics

## What Are Variant Sets?

Variant sets let you define **alternative representations** for a prim and switch between them without duplicating data. Typical uses include model shapes, materials or looks, and LODs. When you select a variant, USD composes the opinions authored for that variant at the prim where the variant set is defined.

### How Does It Work?

A prim can have **one or more** named variant sets. Each variant set contains **variants** (choices). A **variant selection** can be authored on the same layer that defines the set or in a **different layer** that references the prim, so each reference can pick a different option. You author data “inside a variant” by selecting it and opening a **variant edit context**; opinions authored in that context apply only when that variant is active. Standard strength ordering rules still apply; we will dive deeper into LIVRPS later. 

### Working With Python

The essential APIs live on `UsdPrim`, `UsdVariantSets`, and `UsdVariantSet`:

```python
# On a prim:
prim.GetVariantSets() # -> UsdVariantSets
vsets = prim.GetVariantSets()
vset  = vsets.AddVariantSet("name")  # -> UsdVariantSet (create or get)
vset.AddVariant("ChoiceA")  # add a variant
vset.SetVariantSelection("ChoiceA") # select a variant

# Author opinions inside a variant:
with vset.GetVariantEditContext():
    # All specs authored in this 'with' go inside the selected variant
    ...

# Other useful calls:
vset.GetVariantNames()  # ["ChoiceA", "ChoiceB", ...]
vset.GetVariantSelection()  # currently selected name or ""
vset.ClearVariantSelection()  # remove selection at edit target
```

## Key Takeaways
* A variant set provides named choices for a prim. A variant is one choice. Selecting a variant composes the opinions authored for that choice at that prim. 

* Author data inside a variant by selecting it and using GetVariantEditContext(). Those opinions only apply when that variant is active. 

* Variant selections can be authored in different layers, letting each reference pick a different option. Overall results still follow USD strength ordering; covered in more depth in a later lesson.