#!/usr/bin/env python3
"""Deterministic glue for the inference-driven /generate-quiz pipeline.

The INFERENCE (authoring + adversarial verification of fresh questions) is done by
sub-agents that /generate-quiz spawns. This script handles only the mechanical parts:

  plan      compute the fresh/reuse split (<=20% reuse) + per-domain quotas, and dump an
            "avoid-duplication" list of existing stems for the author agents.
  assemble  take the verified fresh questions, validate + resolve their sources, drop any
            duplicates, pick the <=20% reuse set from the bank, write the ordered quiz
            JSON for `generate_quiz.py --from`, and APPEND the fresh questions to the bank.

Usage:
  uv run python exam/quiz_pipeline.py plan     --count 60 --difficulty hard --seed 2027
  uv run python exam/quiz_pipeline.py assemble --fresh exam/output/_fresh-2027.json \
                                               --count 60 --difficulty hard --seed 2027
"""
from __future__ import annotations
import argparse, json, math, random, re, statistics, sys
from pathlib import Path

import generate_quiz as g  # reuse largest_remainder, DOMAIN_WEIGHTS, source rules

HERE = Path(__file__).resolve().parent
BANK = HERE / "question_bank.json"
SMAP = HERE / "source_map.json"
OUT = HERE / "output"
REUSE_FRACTION = 0.20


def _norm(s: str) -> str:
    return " ".join(str(s).lower().split())


_PY_HINTS = ("math.", "CreateInput", "CreateAttribute", "AddRotate", ".Set(", "shader.",
             "usd_mesh", "import ", "def extract", "UsdGeom.", "UsdShade.", "= 1 -")


def _norm_snippets(q):
    """Coerce a question's snippets to a list of {filename, code} (some are authored as
    bare code strings)."""
    out = []
    for s in (q.get("snippets") or []):
        if isinstance(s, dict) and "code" in s:
            fn = s.get("filename") or ("example.py" if any(h in s["code"] for h in _PY_HINTS) else "example.usda")
            out.append({"filename": fn, "code": s["code"]})
        else:
            code = s if isinstance(s, str) else str(s)
            out.append({"filename": "example.py" if any(h in code for h in _PY_HINTS) else "example.usda", "code": code})
    if out:
        q["snippets"] = out
    return q


def _shuffle_choices(q, rng):
    """Randomize option order and remap answer letters, so the correct answer isn't always
    in the same position. Preserves correctness (the correct option text stays correct)."""
    n = len(q["choices"])
    order = list(range(n))
    rng.shuffle(order)
    L = "ABCDE"
    old_index = {L[i]: i for i in range(n)}
    new_pos = {old_i: new_i for new_i, old_i in enumerate(order)}
    q["choices"] = [q["choices"][i] for i in order]
    q["answer"] = sorted(L[new_pos[old_index[a]]] for a in q["answer"])
    return q


def _pool(bank, difficulty):
    return [q for q in bank if q["difficulty"] == difficulty] if difficulty in ("medium", "hard") else bank


# ---------------- distractor-quality lint (style contract: official study-guide samples) ---
# See exam/_verification/official_sample_style.txt for the rules R1-R6 these checks enforce.

_META_RX = re.compile(r"\b(all|none|any|combinations?|both|either|neither)\s+of\s+the\s+above\b"
                      r"|\ball\s+of\s+these\b|\bboth\s+[A-E]\s+and\s+[A-E]\b", re.I)
_LETTER_RX = re.compile(r"(?<![A-Za-z])\(?[A-E]\)?(?:\s+(?:is|are|only|inverts|describes|confuses))"
                        r"|\boption\s+[A-E]\b|\banswers?\s+[A-E]\b|\bchoice\s+[A-E]\b")
_QUAL_RX = re.compile(r"\b(always|never|cannot|impossible|guarantees?|all|only|must)\b", re.I)
_STOP = set("the a an of to in for and or is are be that which with on by as it its from when "
            "what how this you your should can may where while because so if not no".split())


def _cwords(s):
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9_:.]+", s.lower())) - _STOP


def lint_question(q):
    """Return a list of (code, detail) flags for one question. Empty list == clean."""
    flags = []
    ch = q["choices"]
    ci = sorted(ord(c) - 65 for c in q["answer"])
    di = [i for i in range(len(ch)) if i not in ci]
    # R4: meta-options / letter references anywhere
    for i, c in enumerate(ch):
        if _META_RX.search(c):
            flags.append(("meta_option", f"choice {i}: {c[:60]!r}"))
    if _LETTER_RX.search(q.get("explanation", "")):
        flags.append(("letter_ref", "explanation references option letters"))
    if not di:
        return flags
    # R1: length parity — a correct option may not be the unique longest by >1.4x median distractor
    lens = [len(c) for c in ch]
    med = statistics.median(lens[i] for i in di)
    for i in ci:
        if lens[i] == max(lens) and med > 0 and lens[i] > 1.4 * med:
            flags.append(("length_gradient", f"correct option {lens[i]} chars vs distractor median {med:.0f}"))
            break
    # R5: stem-echo — correct option uniquely mirrors the stem's wording
    sw = _cwords(q["stem"])
    if sw:
        ov = [len(_cwords(c) & sw) / max(1, len(_cwords(c))) for c in ch]
        co, do = max(ov[i] for i in ci), max(ov[i] for i in di)
        if co >= 0.5 and co - do >= 0.3:
            flags.append(("stem_echo", f"correct overlap {co:.2f} vs best distractor {do:.2f}"))
    # R6: tone parity — extreme qualifiers in a majority of distractors but no correct option
    qd = sum(1 for i in di if _QUAL_RX.search(ch[i]))
    qc = sum(1 for i in ci if _QUAL_RX.search(ch[i]))
    if qc == 0 and qd >= max(2, len(di) - 1) and len(di) >= 3:
        flags.append(("qualifier_asymmetry", f"{qd}/{len(di)} distractors carry extreme qualifiers, key has none"))
    return flags


def cmd_lint(a):
    src = Path(a.file) if a.file else BANK
    qs = json.load(open(src, encoding="utf-8"))
    flagged = 0
    for q in qs:
        flags = lint_question(q)
        if flags:
            flagged += 1
            for code, detail in flags:
                print(f"{q.get('id','?'):>14}  {code:<20} {detail}")
    print(f"\nlint: {flagged}/{len(qs)} questions flagged in {src.name}")
    sys.exit(1 if flagged and not a.warn_only else 0)


def cmd_plan(a):
    bank = json.load(open(BANK, encoding="utf-8"))
    W = g.DOMAIN_WEIGHTS
    reuse = math.floor(REUSE_FRACTION * a.count)
    fresh = a.count - reuse
    if a.domain:
        fresh_q, reuse_q = {a.domain: fresh}, {a.domain: reuse}
    else:
        big = {d: 10**6 for d in W}
        fresh_q = g.largest_remainder(fresh, W, big)
        avail = {d: sum(1 for q in _pool(bank, a.difficulty) if q["domain"] == d) for d in W}
        reuse_q = g.largest_remainder(reuse, W, avail)
    avoid = {d: [q["stem"] for q in bank if q["domain"] == d] for d in W}
    plan = {
        "count": a.count, "difficulty": a.difficulty, "domain": a.domain, "seed": a.seed,
        "reuse": reuse, "fresh": fresh, "fresh_quota": fresh_q, "reuse_quota": reuse_q,
        "valid_source_keys": sorted(json.load(open(SMAP, encoding="utf-8")).keys()),
        "avoid_stems": avoid,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    pf = OUT / f"_plan-{a.seed}.json"
    json.dump(plan, open(pf, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"PLAN seed={a.seed} count={a.count} difficulty={a.difficulty}: fresh={fresh} reuse={reuse}")
    print("fresh per domain:", {d: n for d, n in fresh_q.items() if n})
    print("reuse per domain:", {d: n for d, n in reuse_q.items() if n})
    print("plan file:", pf)


def cmd_assemble(a):
    bank = json.load(open(BANK, encoding="utf-8"))
    smap = json.load(open(SMAP, encoding="utf-8"))
    fresh = json.load(open(a.fresh, encoding="utf-8"))
    rng = random.Random(a.seed)

    bank_stems = {_norm(q["stem"]) for q in bank}
    clean, errs, seen = [], [], set()
    for i, q in enumerate(fresh):
        miss = [k for k in ("domain", "objective", "difficulty", "type", "stem",
                            "choices", "answer", "explanation", "source") if k not in q]
        if miss:
            errs.append(f"fresh[{i}] missing {miss}"); continue
        if q["source"] not in smap:
            errs.append(f"fresh[{i}] ({q.get('id','?')}) invalid source '{q['source']}'"); continue
        if not (4 <= len(q["choices"]) <= 5):
            errs.append(f"fresh[{i}] bad choice count"); continue
        q.setdefault("select_n", len(q["answer"]) if q["type"] == "multi" else 1)
        if q["type"] == "multi" and len(q["answer"]) != q["select_n"]:
            errs.append(f"fresh[{i}] multi select_n mismatch"); continue
        ns = _norm(q["stem"])
        if ns in bank_stems or ns in seen:
            continue  # silently drop duplicates
        seen.add(ns)
        q["source_ref"] = smap[q["source"]]
        style = lint_question(q)
        hard = [f for f in style if f[0] in ("meta_option", "letter_ref")]
        if hard:
            errs.append(f"fresh[{i}] ({q.get('id','?')}) {hard[0][0]}: {hard[0][1]}"); continue
        for code, detail in style:
            print(f"WARN fresh[{i}] ({q.get('id','?')}) {code}: {detail}", file=sys.stderr)
        _norm_snippets(q)
        if "id" not in q or any(b["id"] == q["id"] for b in bank):
            q["id"] = f"gen{a.seed}-{len(clean)+1:03d}"
        clean.append(q)
    if errs:
        print("FRESH VALIDATION ERRORS — not assembling:", file=sys.stderr)
        for e in errs[:30]:
            print("  ", e, file=sys.stderr)
        sys.exit(1)

    # reuse: <=20%, weighted by domain, prefer items whose (domain,objective) a fresh item didn't cover
    fresh_keys = {(q["domain"], q["objective"]) for q in clean}
    pool = _pool(bank, a.difficulty)
    reuse_n = min(a.reuse if a.reuse is not None else math.floor(REUSE_FRACTION * a.count), len(pool))
    if a.domain:
        cand = [q for q in pool if q["domain"] == a.domain]; rng.shuffle(cand)
        cand.sort(key=lambda q: (q["domain"], q["objective"]) in fresh_keys)
        reused = cand[:reuse_n]
    else:
        avail = {d: [q for q in pool if q["domain"] == d] for d in g.DOMAIN_WEIGHTS}
        quota = g.largest_remainder(reuse_n, g.DOMAIN_WEIGHTS, {d: len(v) for d, v in avail.items()})
        reused = []
        for d, n in quota.items():
            c = avail[d][:]; rng.shuffle(c)
            c.sort(key=lambda q: (q["domain"], q["objective"]) in fresh_keys)
            reused += c[:n]

    quiz = clean + reused
    rng.shuffle(quiz)
    # de-bias answer position on deep copies so the appended bank originals stay intact
    quiz = [_shuffle_choices(json.loads(json.dumps(q)), rng) for q in quiz]
    OUT.mkdir(parents=True, exist_ok=True)
    qp = OUT / f"quiz-{a.seed}.json"
    json.dump(quiz, open(qp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # grow the pool with verified fresh questions, stored de-biased (shuffled option order)
    bank.extend(_shuffle_choices(json.loads(json.dumps(q)), rng) for q in clean)
    json.dump(bank, open(BANK, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    share = len(clean) / len(quiz) if quiz else 0
    print(f"assembled {len(quiz)} questions = {len(clean)} fresh ({round(100*share)}%) "
          f"+ {len(reused)} reused ({round(100*(1-share))}%)")
    print(f"quiz file: {qp}")
    print(f"bank grew to {len(bank)} questions")
    if share < 0.80:
        print(f"WARN: fresh share {round(100*share)}% is below the 80% target", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="Deterministic glue for the /generate-quiz inference pipeline.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("plan")
    pp.add_argument("--count", type=int, default=60)
    pp.add_argument("--difficulty", choices=["mixed", "medium", "hard"], default="mixed")
    pp.add_argument("--domain", default=None)
    pp.add_argument("--seed", type=int, required=True)
    pp.set_defaults(func=cmd_plan)
    pa = sub.add_parser("assemble")
    pa.add_argument("--fresh", required=True, help="JSON list of verified fresh questions")
    pa.add_argument("--count", type=int, default=60)
    pa.add_argument("--difficulty", choices=["mixed", "medium", "hard"], default="mixed")
    pa.add_argument("--domain", default=None)
    pa.add_argument("--seed", type=int, required=True)
    pa.add_argument("--reuse", type=int, default=None, help="override reuse count (default floor(0.2*count))")
    pa.set_defaults(func=cmd_assemble)
    pl = sub.add_parser("lint", help="distractor-quality lint (official sample style contract)")
    pl.add_argument("--file", default=None, help="quiz/bank JSON to lint (default: question_bank.json)")
    pl.add_argument("--warn-only", action="store_true", help="always exit 0")
    pl.set_defaults(func=cmd_lint)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
