import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_DIR = Path(tempfile.gettempdir()) / "openusd"

JUPYTEXT_MARKER = re.compile(r"^jupytext:", re.MULTILINE)


def find_jupytext_files(docs_dir: Path) -> list[Path]:
    """Find all .md files containing Jupytext frontmatter."""
    results = []
    for md_file in docs_dir.rglob("*.md"):
        if ".ipynb_checkpoints" in md_file.parts:
            continue
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if JUPYTEXT_MARKER.search(text):
            results.append(md_file)
    return sorted(results)


def convert_files(files: list[Path]) -> None:
    """Convert Jupytext .md files to .ipynb, preserving directory structure."""
    for md_file in files:
        rel = md_file.relative_to(DOCS_DIR)
        out_dir = OUTPUT_DIR / rel.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / rel.with_suffix(".ipynb").name
        print(f"  {rel} -> {out_file}")
        subprocess.run(
            [sys.executable, "-m", "jupytext", "--to", "notebook", str(md_file), "-o", str(out_file)],
            check=True,
        )


def main() -> None:
    print(f"==> Finding Jupytext .md files in {DOCS_DIR}...")
    files = find_jupytext_files(DOCS_DIR)
    print(f"    Found {len(files)} files.")

    print(f"\n==> Converting to .ipynb in {OUTPUT_DIR}...")
    convert_files(files)

    print(f"\n==> Launching JupyterLab at {OUTPUT_DIR}...")
    subprocess.run(
        [sys.executable, "-m", "jupyter", "lab", f"--notebook-dir={OUTPUT_DIR}"],
        check=True,
    )


if __name__ == "__main__":
    main()
