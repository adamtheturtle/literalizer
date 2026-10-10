"""Retry transient linkcheck HTTP failures after a bounded delay."""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path


def _only_transient_failures(output: Path) -> bool:
    """Require actual broken links and only HTTP 502/504 failures."""
    try:
        entries: list[dict[str, str]] = [
            json.loads(s=line)
            for line in output.read_text(encoding="utf-8").splitlines()
        ]
        failures = [
            entry
            for entry in entries
            if entry["status"]
            not in {"working", "ignored", "redirected", "unchecked"}
        ]
        return bool(failures) and all(
            entry["status"] == "broken"
            and re.match(
                pattern=r"(?:502|504) Server Error:", string=entry["info"]
            )
            is not None
            for entry in failures
        )
    except (OSError, ValueError, KeyError, TypeError):
        return False


def run(source: Path, build: Path, doctrees: Path, retry_delay: float) -> int:
    """Repeat one full linkcheck only for transient HTTP failures."""
    report = build / "linkcheck" / "output.json"
    for attempt in range(2):
        # A failed build must never be classified using a previous report.
        report.unlink(missing_ok=True)
        result = subprocess.run(
            args=[
                sys.executable,
                "-m",
                "sphinx",
                "-M",
                "linkcheck",
                str(object=source),
                str(object=build),
                "-W",
                "-E",
                "-d",
                str(object=doctrees),
            ],
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=600,
        )
        _ = sys.stderr.write(result.stderr)
        if (
            result.returncode != 1
            or result.stderr != ""
            or attempt == 1
            or not _only_transient_failures(output=report)
        ):
            return result.returncode
        _ = sys.stderr.write(
            "Retrying linkcheck after HTTP 502/504 failures "
            f"in {retry_delay}s.\n"
        )
        time.sleep(retry_delay)
    return 1


def main() -> None:
    """Check the given documentation source and build directories."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("source", type=Path)
    _ = parser.add_argument("build", type=Path)
    _ = parser.add_argument("doctrees", type=Path)
    _ = parser.add_argument("--retry-delay", type=float, default=10)
    args = parser.parse_args()
    sys.exit(
        run(
            source=args.source,
            build=args.build,
            doctrees=args.doctrees,
            retry_delay=args.retry_delay,
        )
    )


if __name__ == "__main__":
    main()
