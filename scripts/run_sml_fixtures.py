"""Compile SML fixtures by content and execute every cached program."""

import argparse
import concurrent.futures
import hashlib
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_LOGGER = logging.getLogger(name=__name__)


def find_mlton() -> str:
    """Require the pinned compiler installed by the native job."""
    compiler = shutil.which(cmd="mlton")
    if compiler is None:
        msg = "MLton executable was not found."
        raise RuntimeError(msg)
    return compiler


def run_fixture(
    *, fixture: Path, cache_dir: Path, compiler: str, rebuild: bool
) -> bool:
    """Reuse compilation by source content, then always execute assertions.

    The workflow separates caches by compiler, runner image and this helper.
    A private build directory and atomic replacement also support duplicate
    fixture contents being compiled concurrently.
    """
    source = fixture.read_bytes()
    digest = hashlib.sha256(string=source).hexdigest()
    program = cache_dir / digest
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_hit = program.is_file() and not rebuild
    try:
        if not cache_hit:
            with tempfile.TemporaryDirectory(
                prefix=".build-", dir=cache_dir
            ) as temporary:
                directory = Path(temporary)
                input_path = directory / "check.sml"
                output_path = directory / "program"
                _ = input_path.write_bytes(data=source)
                _ = subprocess.run(
                    args=[
                        compiler,
                        "-output",
                        str(object=output_path),
                        str(object=input_path),
                    ],
                    check=True,
                )
                _ = output_path.replace(target=program)
        _ = subprocess.run(args=[str(object=program)], check=True)
    except (subprocess.CalledProcessError, OSError) as error:
        msg = f"SML fixture failed: {fixture}"
        raise RuntimeError(msg) from error
    return cache_hit


def main() -> None:
    """Read NUL-separated paths and retain the native job's
    parallelism.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--cache-dir", type=Path, default=Path(".cache/sml-programs")
    )
    _ = parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    fixtures = [
        Path(os.fsdecode(filename=name))
        for name in sys.stdin.buffer.read().split(sep=b"\0")
        if name != b""
    ]
    if len(fixtures) == 0:
        parser.error(message="No SML fixtures were supplied.")
    workers = os.cpu_count()
    if workers is None:
        workers = 1
    compiler = find_mlton()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers
    ) as executor:
        futures = [
            executor.submit(
                run_fixture,
                fixture=fixture,
                cache_dir=args.cache_dir,
                compiler=compiler,
                rebuild=args.rebuild,
            )
            for fixture in fixtures
        ]
        hits = [future.result() for future in futures]
    _LOGGER.info(
        "Executed %s SML fixtures: %s cached, %s compiled.",
        len(fixtures),
        sum(hits),
        len(hits) - sum(hits),
    )


if __name__ == "__main__":
    main()
