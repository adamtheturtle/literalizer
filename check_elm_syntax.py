"""Check syntax of Elm golden files using ``elm make``."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_ELM_JSON = json.dumps(
    obj={
        "type": "application",
        "source-directories": ["src"],
        "elm-version": "0.19.1",
        "dependencies": {
            "direct": {"elm/core": "1.0.5"},
            "indirect": {"elm/json": "1.1.3"},
        },
        "test-dependencies": {"direct": {}, "indirect": {}},
    },
)


def main() -> None:
    """Check syntax of each given Elm golden file."""
    elm_path = shutil.which(cmd="elm") or "elm"
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        elm_json_path = Path(tmpdir) / "elm.json"
        elm_json_path.write_text(data=_ELM_JSON, encoding="utf-8")
        for filename in sys.argv[1:]:
            src = Path(filename)
            target = src_dir / "Check.elm"
            target.write_text(
                data=src.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = subprocess.run(
                args=[elm_path, "make", "src/Check.elm", "--output=/dev/null"],
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
            )
            if result.returncode != 0:
                msg = (
                    f"{filename}: elm make failed\n"
                    f"{result.stderr}{result.stdout}"
                )
                sys.stderr.write(msg)
                sys.exit(1)


if __name__ == "__main__":
    main()
