# /generate-quiz

Generate an NCP-OUSD practice test where **every quiz is freshly authored by inference each run**
(≥80% brand-new questions, ≤20% reused from the bank). Fresh questions are source-grounded and
adversarially verified before they ship, then appended to the bank so the pool grows.

Arguments: $ARGUMENTS

> This is NOT a static sampler. Each run uses inference (sub-agents) to write new questions, so it
> takes ~2-5 minutes and real tokens. That is intended.

## Argument parsing
Parse `$ARGUMENTS` (any order, all optional):
- bare integer → `count` (default **60**; official exam is 60-70)
- `medium` | `hard` | `mixed` → `difficulty` (default **mixed**)
- `domain:<Name>` → focus one domain (canonical: Composition, Content Aggregation, Customizing USD,
  Data Exchange, Data Modeling, Debugging and Troubleshooting, Pipeline Development, Visualization)
- `seed:<int>` → seed (default: pick a fresh integer and state it)

## Pipeline (run these steps in order)

### 1. Plan the split
```
uv run python exam/quiz_pipeline.py plan --count <count> --difficulty <difficulty> [--domain "<D>"] --seed <seed>
```
This writes `exam/output/_plan-<seed>.json` with `fresh_quota` (per-domain counts to author),
`reuse_quota`, `valid_source_keys`, and `avoid_stems` (existing stems to NOT duplicate). Read it.

### 2. Author fresh questions (INFERENCE — parallel sub-agents, split by domain)
Spawn parallel `general-purpose` agents (group domains like the bank build: Comp+Debug / Agg+Pipeline /
Modeling+Viz+Customizing / Data Exchange). Give each agent its domains' `fresh_quota`, the
`avoid_stems` for those domains, and these rules:
- Author exactly the quota of NEW questions per domain at the requested `difficulty`.
- Ground every question ONLY in the verified corpus: page text in `exam/_verification/pages/<key>` and
  `exam/_verification/pages_official/<key>.txt`; set `source` to a key from `valid_source_keys` and
  VERIFY the fact by grepping that page. No fact may come from memory.
- Official self-contained voice (see Style below). Do NOT reference exercises/lessons/figures.
- Do NOT duplicate any `avoid_stems` entry or each other; diversify objectives within the domain.
- Output full schema objects: `{domain, objective, difficulty, type, select_n, stem, snippets?, choices,
  answer, explanation, source}`. choices are plain (no letters); answer is letters (A=choices[0]…);
  multi-select needs ≥1 plausible-but-wrong distractor. Write each group's array to
  `exam/_bank_parts/_fresh_<group>.json`.
- **Explanations MUST reference option CONTENT, never bare letters** ("the prepend distractor only
  orders…", NOT "(B) only orders…"). Option order is shuffled at render, so any letter reference
  becomes wrong. Also vary which option is correct (don't always key the first choice).
- **Distractor style contract (official sample style — see
  `exam/_verification/official_sample_style.txt`, rules R1-R6; lint enforces these):**
  - Every distractor is a REAL USD attribute/schema/arc/behavior misapplied, a direction/strength/
    order flip, a neighbor concept's true purpose, or a real rule misapplied — NEVER an invented
    absurdity, and an option must NEVER explain its own wrongness ("…so they cannot be changed").
  - Parallel grammar + matched length: options share a sentence template; the correct option must
    not be the longest by >1.3x the median distractor length.
  - No "all/none/combinations of the above", no letter references in options.
  - No stem-echo: the correct option must not uniquely reuse a distinctive 3+ word stem phrase.
  - Tone parity: extreme qualifiers (always/never/cannot/only) must not mark only distractors.
  - Multi-select: distractors are the same KIND of item as the keys (real attributes that simply
    aren't required, real pairs that don't need sync) and individually, definitively wrong.

### 3. Adversarially verify every fresh question (INFERENCE — parallel skeptics)
Spawn verifier agents. For each fresh candidate, the skeptic re-reads the cited source page and tries to
REFUTE it: is the keyed answer actually correct per the source? is every distractor actually wrong? is
it self-contained and structurally valid (4-5 choices, answer matches select_n)? Mark each verdict
`pass`/`fail` with a reason. **Drop every `fail`.** If dropping leaves a domain under its quota, send the
author agent back to top-up (repeat until quotas are met by passing items only). Concatenate all passing
fresh questions into one `exam/output/_fresh-<seed>.json`.

### 4. Assemble + grow the bank + render
```
uv run python exam/quiz_pipeline.py assemble --fresh exam/output/_fresh-<seed>.json --count <count> --difficulty <difficulty> [--domain "<D>"] --seed <seed>
uv run python exam/quiz_pipeline.py lint --file exam/output/quiz-<seed>.json
uv run python exam/generate_quiz.py --from exam/output/quiz-<seed>.json --difficulty <difficulty> [--domain "<D>"] --seed <seed> --md
```
`assemble` validates the fresh set (hard-rejects meta-options/letter refs; warns on style flags),
drops duplicates, picks the ≤20% reuse set, writes `exam/output/quiz-<seed>.json`, and APPENDS the
fresh questions to `question_bank.json`. `lint` is the distractor-quality gate — if it flags any
question, send those back to the author agents for repair and re-assemble before rendering. The
final command renders the PDF (and a Markdown sidecar).

### 5. Report
State: the fresh/reuse split (must be ≥80% fresh), how many candidates failed verification and why,
the domain distribution, the new bank size, and the PDF path. Offer to open the PDF.

## Style (official voice — match the study-guide samples)
Self-contained, concise (prose stems ≤~220 chars), generic-professional or direct-conceptual. Exemplars:
"What is the primary purpose of the defaultPrim metadata in a USD layer?"; "You have a UsdGeomMesh with
1,000 vertices and 500 faces… What should be the length of the faceVertexIndices array?". No tutorial
references, no narrative props (warehouses/pallets/named artists).

## Contract / notes
- **Inference every run; ≤20% reuse** enforced by `quiz_pipeline.py` (`floor(0.2*count)`); it warns if the
  fresh share drops below 80%.
- Every shipped question carries a verified primary-source citation; `generate_quiz.py` skips any
  unsourced question. Sources resolve via `exam/source_map.json`; exam facts (weights/duration) from
  `exam/official_guidelines.json`.
- Fresh questions are appended to `exam/question_bank.json` (deduped by stem), so the reuse pool deepens.
- Examples: `/generate-quiz` · `/generate-quiz 70 hard` · `/generate-quiz domain:Composition 20` ·
  `/generate-quiz 60 hard seed:7`.
