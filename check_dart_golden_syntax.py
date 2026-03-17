"""Check syntax of Dart golden files using dart analyze."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Dart golden file."""
    dart_path = shutil.which(cmd="dart")

    if dart_path is None:
        return
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            pubspec = tmpdir_path / "pubspec.yaml"
            pubspec.write_text(
                data="name: check\nenvironment:\n  sdk: ^3.0.0\n",
                encoding="utf-8",
            )
            dart_file = tmpdir_path / "check.dart"
            dart_file.write_text(data=content, encoding="utf-8")
            dart_file_path = dart_file.as_posix()
            result = subprocess.run(
                args=[dart_path, "analyze", "--fatal-infos", dart_file_path],
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode != 0:
            output = f"{result.stderr}{result.stdout}"
            msg = f"{filename}: Dart syntax error\n{output}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
