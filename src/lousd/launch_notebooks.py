import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "docs" / "_build" / "html" / "notebooks"


def main() -> None:
    if not NOTEBOOKS_DIR.exists():
        print(f"Error: {NOTEBOOKS_DIR} not found.")
        print("Run the Sphinx build first: uv run sphinx-build -M html docs/ docs/_build/")
        sys.exit(1)

    print(f"==> Launching JupyterLab at {NOTEBOOKS_DIR}...")
    subprocess.run(
        [sys.executable, "-m", "jupyter", "lab", f"--notebook-dir={NOTEBOOKS_DIR}"],
        check=True,
    )

