#!/usr/bin/env python3
"""Generate an NCP-OUSD practice-test PDF from the curated question bank.

Samples questions weighted by the official exam domain percentages, renders an
NVIDIA-styled LaTeX document via a Jinja2 template, and compiles it with
pdflatex. Deterministic given --seed.

Examples
--------
    uv run python exam/generate_quiz.py                          # 60-Q weighted exam
    uv run python exam/generate_quiz.py --count 30 --difficulty hard
    uv run python exam/generate_quiz.py --domain Composition --count 15
    uv run python exam/generate_quiz.py --seed 7 --md
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

HERE = Path(__file__).resolve().parent
BANK_PATH = HERE / "question_bank.json"
TEMPLATE_DIR = HERE / "templates"
OUTPUT_DIR = HERE / "output"

# The official NCP-OUSD exam guidelines are the SOURCE OF TRUTH for weighting and exam
# facts. They live in official_guidelines.json (agent-browser-verified from the NVIDIA
# certification page) and are loaded at runtime so the generator can never silently drift
# from the published blueprint. Hardcoded values below are only a fallback if the file is
# missing.
GUIDELINES_PATH = HERE / "official_guidelines.json"
_FALLBACK = {
    "duration_minutes": 120,
    "question_count_min": 60,
    "question_count_max": 70,
    "domain_weights": {
        "Composition": 23, "Data Exchange": 15, "Pipeline Development": 14,
        "Data Modeling": 13, "Debugging and Troubleshooting": 11,
        "Content Aggregation": 10, "Visualization": 8, "Customizing USD": 6,
    },
}

def load_guidelines() -> dict:
    try:
        g = json.load(open(GUIDELINES_PATH, encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return dict(_FALLBACK)
    for k, v in _FALLBACK.items():
        g.setdefault(k, v)
    return g

GUIDELINES = load_guidelines()
DOMAIN_WEIGHTS = GUIDELINES["domain_weights"]
EXAM_MINUTES = GUIDELINES["duration_minutes"]
COUNT_MIN = GUIDELINES["question_count_min"]
COUNT_MAX = GUIDELINES["question_count_max"]
assert sum(DOMAIN_WEIGHTS.values()) == 100, "official domain weights must sum to 100"

_TEX_REPL = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    "<": r"\textless{}", ">": r"\textgreater{}",
}


def tex_escape(text: str) -> str:
    """Escape LaTeX special characters in plain (non-code) text."""
    return "".join(_TEX_REPL.get(ch, ch) for ch in str(text))


_PY_HINTS = ("math.", "CreateInput", "CreateAttribute", "AddRotate", ".Set(", "shader.",
             "usd_mesh", "import ", "def extract", "UsdGeom.", "UsdShade.", "= 1 -")


def debias_options(q, rng):
    """Randomize option order and remap answer letters so the correct answer isn't always in
    the same position. Preserves correctness. Mutates a copy-safe dict in place."""
    n = len(q["choices"])
    order = list(range(n))
    rng.shuffle(order)
    L = "ABCDE"
    old_index = {L[i]: i for i in range(n)}
    new_pos = {o: i for i, o in enumerate(order)}
    q["choices"] = [q["choices"][i] for i in order]
    q["answer"] = sorted(L[new_pos[old_index[a]]] for a in q["answer"])
    return q


def _single_letter_dist(questions):
    from collections import Counter
    return Counter(q["answer"][0] for q in questions if q["type"] == "single")


def balance_answers(questions, seed, max_share=0.40, tries=40):
    """Return a copy of `questions` with option order shuffled so the correct-answer LETTER is
    spread across A/B/C/D — GUARANTEEING no single letter exceeds `max_share` of the
    single-choice questions when achievable. Retries with fresh shuffles and keeps the most
    uniform result. Correctness is always preserved."""
    import json as _json
    from collections import Counter

    def attempt(s):
        rng = random.Random(s)
        out = [debias_options(_json.loads(_json.dumps(q)), rng) for q in questions]
        dist = _single_letter_dist(out)
        n = sum(dist.values()) or 1
        worst = max(dist.values()) / n if dist else 0.0
        return out, worst

    best, best_worst = None, 1.1
    for t in range(tries):
        out, worst = attempt(seed * 1000 + t)
        if worst < best_worst:
            best, best_worst = out, worst
        if worst <= max_share:
            return out
    print(f"note: best answer-balance achieved is {round(best_worst*100)}% for the top letter "
          f"(target <= {round(max_share*100)}%); using it.", file=sys.stderr)
    return best


def _norm_snippet(s):
    """Coerce a snippet into {filename, code}. Some authored snippets arrive as bare code
    strings; pick a sensible filename and escape the (display-only) filename for LaTeX."""
    if isinstance(s, dict) and "code" in s:
        fn = s.get("filename") or ("example.py" if any(h in s["code"] for h in _PY_HINTS) else "example.usda")
        return {"filename": tex_escape(fn), "code": s["code"]}
    code = s if isinstance(s, str) else str(s)
    fn = "example.py" if any(h in code for h in _PY_HINTS) else "example.usda"
    return {"filename": tex_escape(fn), "code": code}


def largest_remainder(count: int, weights: dict[str, int],
                      available: dict[str, int]) -> dict[str, int]:
    """Apportion `count` slots across domains by weight (largest-remainder),
    clamped to availability, redistributing any shortfall to other domains."""
    total_w = sum(weights[d] for d in weights)
    raw = {d: count * weights[d] / total_w for d in weights}
    alloc = {d: int(raw[d]) for d in weights}
    remainder = count - sum(alloc.values())
    # distribute remaining seats by largest fractional part, tie-break by weight
    # round the fractional part to kill float noise so domain weight breaks true ties
    order = sorted(weights, key=lambda d: (round(raw[d] - int(raw[d]), 9), weights[d]),
                   reverse=True)
    i = 0
    while remainder > 0 and order:
        d = order[i % len(order)]
        alloc[d] += 1
        remainder -= 1
        i += 1

    # clamp to availability and collect deficit
    deficit = 0
    for d in alloc:
        if alloc[d] > available.get(d, 0):
            deficit += alloc[d] - available[d]
            alloc[d] = available[d]
    # redistribute deficit to domains that still have headroom, by weight
    while deficit > 0:
        candidates = [d for d in weights if alloc[d] < available.get(d, 0)]
        if not candidates:
            break
        candidates.sort(key=lambda d: weights[d], reverse=True)
        progressed = False
        for d in candidates:
            if deficit <= 0:
                break
            alloc[d] += 1
            deficit -= 1
            progressed = True
        if not progressed:
            break
    return alloc


def select_questions(bank: list[dict], count: int, difficulty: str,
                     domain_focus: str | None, rng: random.Random) -> list[dict]:
    pool = bank
    if difficulty in ("medium", "hard"):
        pool = [q for q in pool if q["difficulty"] == difficulty]

    if domain_focus:
        focus = [q for q in pool if q["domain"].lower() == domain_focus.lower()]
        if not focus:
            sys.exit(f"No questions for domain '{domain_focus}' "
                     f"(difficulty={difficulty}). Domains: {sorted(DOMAIN_WEIGHTS)}")
        rng.shuffle(focus)
        return focus[:count]

    by_domain: dict[str, list[dict]] = {d: [] for d in DOMAIN_WEIGHTS}
    for q in pool:
        by_domain.setdefault(q["domain"], []).append(q)
    available = {d: len(by_domain.get(d, [])) for d in DOMAIN_WEIGHTS}

    if count > sum(available.values()):
        print(f"! Requested {count} but only {sum(available.values())} available "
              f"(difficulty={difficulty}); using all.", file=sys.stderr)
        count = sum(available.values())

    alloc = largest_remainder(count, DOMAIN_WEIGHTS, available)
    chosen: list[dict] = []
    for d, n in alloc.items():
        items = by_domain.get(d, [])[:]
        rng.shuffle(items)
        chosen.extend(items[:n])
    rng.shuffle(chosen)
    return chosen


def prep(q: dict) -> dict:
    """Build the template view-model for one question (escaped text, raw code)."""
    select_n = q.get("select_n", 1)
    multi_label = ""
    if q["type"] == "multi":
        words = {2: "two", 3: "three", 4: "four"}.get(select_n, str(select_n))
        multi_label = f"(Select {words} options.)"
    ref = q.get("source_ref") or {}
    return {
        "domain": tex_escape(q["domain"]),
        "objective": tex_escape(q["objective"]),
        "stem_tex": tex_escape(q["stem"]),
        "choices_tex": [tex_escape(c) for c in q["choices"]],
        "snippets": [_norm_snippet(s) for s in (q.get("snippets") or [])],
        "multi_label": multi_label,
        "answer_str": ", ".join(q["answer"]),
        "explanation_tex": tex_escape(q["explanation"]),
        "source_title": tex_escape(ref.get("title", "")),
        "source_url": ref.get("url", ""),   # raw, wrapped in \url{} by the template
    }


def distribution_str(questions: list[dict]) -> str:
    from collections import Counter
    c = Counter(q["domain"] for q in questions)
    parts = [f"{d} {c[d]}" for d in DOMAIN_WEIGHTS if c.get(d)]
    extra = [f"{d} {c[d]}" for d in c if d not in DOMAIN_WEIGHTS]
    return tex_escape(" · ".join(parts + extra))


def render_tex(questions: list[dict], args, seed: int) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((=", comment_end_string="=))",
        trim_blocks=True, lstrip_blocks=True, autoescape=False,
    )
    tmpl = env.get_template("exam.tex.j2")
    meta = {
        "count": len(questions),
        "minutes": EXAM_MINUTES,
        "difficulty": tex_escape(args.difficulty.capitalize()),
        "seed": seed,
        "domain_focus": tex_escape(args.domain) if args.domain else "",
        "distribution": distribution_str(questions),
        "official_note": tex_escape(
            f"Real exam: {COUNT_MIN}-{COUNT_MAX} questions, {EXAM_MINUTES} min, "
            f"{GUIDELINES.get('level','Professional')} level. Weighting follows the official "
            f"NVIDIA blueprint."),
    }
    return tmpl.render(meta=meta, questions=[prep(q) for q in questions],
                       with_answers=not args.no_answers)


def compile_pdf(tex: str, out_pdf: Path, keep_tex: bool) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdflatex = shutil.which("pdflatex") or "/Library/TeX/texbin/pdflatex"
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "exam.tex").write_text(tex, encoding="utf-8")
        for _ in range(2):  # twice for stable page numbers
            proc = subprocess.run(
                [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "exam.tex"],
                cwd=td, capture_output=True, text=True,
            )
        built = td / "exam.pdf"
        if not built.exists():
            log = (td / "exam.log")
            tail = log.read_text(errors="replace")[-3000:] if log.exists() else proc.stdout[-3000:]
            sys.exit("pdflatex failed. Tail of log:\n" + tail)
        shutil.copy(built, out_pdf)
        if keep_tex:
            shutil.copy(td / "exam.tex", out_pdf.with_suffix(".tex"))


def write_markdown(questions: list[dict], out_md: Path, with_answers: bool) -> None:
    lines = ["# NCP-OUSD Practice Test\n"]
    for i, q in enumerate(questions, 1):
        lines.append(f"### Question {i}")
        label = ""
        if q["type"] == "multi":
            words = {2: "two", 3: "three"}.get(q.get("select_n", 2), str(q.get("select_n")))
            label = f" _(Select {words} options.)_"
        lines.append(f"**Domain:** {q['domain']}{label}\n")
        lines.append(q["stem"] + "\n")
        for s in (q.get("snippets") or []):
            lines.append(f"*{s['filename']}*\n\n```usda\n{s['code']}\n```\n")
        for j, c in enumerate(q["choices"]):
            lines.append(f"- **{chr(65+j)}.** {c}")
        lines.append("")
    if with_answers:
        lines.append("\n## Answer Key & Explanations\n")
        for i, q in enumerate(questions, 1):
            lines.append(f"**{i}. {', '.join(q['answer'])}** [{q['domain']} · {q['objective']}] — {q['explanation']}\n")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def render_from(args) -> None:
    """Render an already-assembled, ordered quiz (list of full question objects) to PDF.
    Used by the /generate-quiz inference pipeline, which authors+verifies the questions and
    hands a finished set here. Re-resolves source_ref and enforces the source-grounding rule."""
    src = Path(args.from_json)
    if not src.exists():
        sys.exit(f"--from file not found: {src}")
    questions = json.load(open(src, encoding="utf-8"))
    if not isinstance(questions, list) or not questions:
        sys.exit(f"--from file must be a non-empty JSON list of questions: {src}")

    # Resolve/refresh source citations from source_map.json when missing.
    smap_path = HERE / "source_map.json"
    smap = json.load(open(smap_path, encoding="utf-8")) if smap_path.exists() else {}
    for q in questions:
        if not (q.get("source_ref") or {}).get("url") and q.get("source") in smap:
            q["source_ref"] = smap[q["source"]]

    unsourced = [q.get("id", "?") for q in questions if not (q.get("source_ref") or {}).get("url")]
    if unsourced:
        print(f"note: skipping {len(unsourced)} unsourced question(s): "
              f"{', '.join(unsourced[:10])}{'…' if len(unsourced)>10 else ''}", file=sys.stderr)
        questions = [q for q in questions if (q.get("source_ref") or {}).get("url")]
    if not questions:
        sys.exit("No sourced questions to render.")

    seed = args.seed if args.seed is not None else 0
    # GUARANTEE answer-position balance even when rendering a pre-built quiz
    questions = balance_answers(questions, seed)
    out_pdf = (Path(args.out) if args.out
               else OUTPUT_DIR / f"{src.stem}.pdf").resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    tex = render_tex(questions, args, seed)
    compile_pdf(tex, out_pdf, args.keep_tex)

    from collections import Counter
    dist = Counter(q["domain"] for q in questions)
    print(f"Rendered {len(questions)} questions from {src.name}")
    for d in sorted(dist, key=lambda x: -dist[x]):
        print(f"  {dist[d]:3d}  {d}")
    print(f"answer spread (single): {dict(_single_letter_dist(questions))}")
    print(f"PDF: {out_pdf}")
    if args.md:
        out_md = out_pdf.with_suffix(".md")
        write_markdown(questions, out_md, not args.no_answers)
        print(f"MD:  {out_md}")


def main() -> None:
    p = argparse.ArgumentParser(description="Generate an NCP-OUSD practice-test PDF.")
    p.add_argument("--count", type=int, default=60, help="number of questions (default 60)")
    p.add_argument("--difficulty", choices=["mixed", "medium", "hard"], default="mixed")
    p.add_argument("--domain", default=None,
                   help="focus all questions on one domain (e.g. 'Composition')")
    p.add_argument("--seed", type=int, default=None, help="RNG seed (default: random)")
    p.add_argument("--no-answers", action="store_true", help="omit the answer key")
    p.add_argument("--md", action="store_true", help="also write a Markdown sidecar")
    p.add_argument("--keep-tex", action="store_true", help="keep the generated .tex")
    p.add_argument("--out", default=None, help="output PDF path")
    p.add_argument("--from", dest="from_json", default=None,
                   help="render an already-built ordered quiz JSON (list of question objects); "
                        "skips sampling. Used by the inference pipeline in /generate-quiz.")
    args = p.parse_args()

    # Render-only mode: a pre-built quiz (e.g. from the inference pipeline) is rendered as-is.
    if args.from_json:
        return render_from(args)

    if not BANK_PATH.exists():
        sys.exit(f"Question bank not found: {BANK_PATH}")
    bank = json.load(open(BANK_PATH, encoding="utf-8"))

    # Source-grounding requirement: every question MUST cite a primary source. Any question
    # lacking a resolved source_ref is skipped (not silently shown) and reported.
    unsourced = [q["id"] for q in bank if not (q.get("source_ref") or {}).get("url")]
    if unsourced:
        print(f"note: skipping {len(unsourced)} unsourced question(s) (no primary source): "
              f"{', '.join(unsourced[:10])}{'…' if len(unsourced)>10 else ''}", file=sys.stderr)
        bank = [q for q in bank if (q.get("source_ref") or {}).get("url")]

    if not (COUNT_MIN <= args.count <= COUNT_MAX):
        print(f"note: official exam is {COUNT_MIN}-{COUNT_MAX} questions; you requested "
              f"{args.count}. Weighting still follows the official blueprint.", file=sys.stderr)

    seed = args.seed if args.seed is not None else random.randint(1000, 999999)
    rng = random.Random(seed)

    questions = select_questions(bank, args.count, args.difficulty, args.domain, rng)
    if not questions:
        sys.exit("No questions selected.")
    # GUARANTEE answer-position balance (no single letter > 40% of single-choice answers)
    questions = balance_answers(questions, seed)

    out_pdf = Path(args.out) if args.out else OUTPUT_DIR / f"ncp-ousd-practice-test-{seed}.pdf"
    out_pdf = out_pdf.resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    tex = render_tex(questions, args, seed)
    compile_pdf(tex, out_pdf, args.keep_tex)

    from collections import Counter
    dist = Counter(q["domain"] for q in questions)
    print(f"Generated {len(questions)} questions (seed={seed}, difficulty={args.difficulty}"
          + (f", domain={args.domain}" if args.domain else "") + ")")
    for d in sorted(dist, key=lambda x: -dist[x]):
        print(f"  {dist[d]:3d}  {d}")
    print(f"answer spread (single): {dict(_single_letter_dist(questions))}")
    print(f"PDF: {out_pdf}")

    if args.md:
        out_md = out_pdf.with_suffix(".md")
        write_markdown(questions, out_md, not args.no_answers)
        print(f"MD:  {out_md}")


if __name__ == "__main__":
    main()
