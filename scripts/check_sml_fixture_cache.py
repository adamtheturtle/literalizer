"""Check SML cache invalidation and assertion failures with the real
compiler.
"""

import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from scripts.run_sml_fixtures import find_mlton, run_fixture

_LOGGER = logging.getLogger(name=__name__)


def _require(*, condition: bool, message: str) -> None:
    """Keep native controls active even when Python assertions are
    disabled.
    """
    if not condition:
        raise AssertionError(message)


def _require_failure(*, fixture: Path, cache: Path, compiler: str) -> None:
    """Require a real compiler or executable failure to propagate."""
    try:
        _ = run_fixture(
            fixture=fixture, cache_dir=cache, compiler=compiler, rebuild=False
        )
    except RuntimeError as error:
        if not isinstance(error.__cause__, subprocess.CalledProcessError):
            raise
    else:
        msg = "A failing SML fixture passed."
        raise AssertionError(msg)


def main() -> None:
    """Prove cached binaries still execute and changed inputs
    recompile.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    compiler = find_mlton()
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        fixture = root / "Sml fixture.sml"
        cache = root / "cache"
        _ = fixture.write_text(
            data='val _ = print "cache control passed\\n"\n'
        )
        _require(
            condition=not run_fixture(
                fixture=fixture,
                cache_dir=cache,
                compiler=compiler,
                rebuild=False,
            ),
            message="The initial compilation was reported as cached.",
        )
        _require(
            condition=run_fixture(
                fixture=fixture,
                cache_dir=cache,
                compiler=compiler,
                rebuild=False,
            ),
            message="An unchanged fixture was not reused.",
        )
        _require(
            condition=not run_fixture(
                fixture=fixture,
                cache_dir=cache,
                compiler=compiler,
                rebuild=True,
            ),
            message="A forced rebuild reused the cached binary.",
        )
        _ = fixture.write_text(
            data='val _ = raise Fail "cache control failed"\n'
        )
        # Fail after compilation and again when reusing the same binary.
        _require_failure(fixture=fixture, cache=cache, compiler=compiler)
        _require_failure(fixture=fixture, cache=cache, compiler=compiler)
        previous = set(cache.iterdir())
        _ = fixture.write_text(data="invalid SML syntax !\n")
        _require_failure(fixture=fixture, cache=cache, compiler=compiler)
        _require(
            condition=set(cache.iterdir()) == previous,
            message="A failed compilation left a partial cache entry.",
        )
        _ = fixture.write_text(data="val _ = ()\n")
        completed = subprocess.run(
            args=[
                sys.executable,
                "-m",
                "scripts.run_sml_fixtures",
                "--cache-dir",
                str(object=cache),
            ],
            input=os.fsencode(filename=fixture) + b"\0",
            capture_output=True,
            check=False,
        )
        _require(
            condition=completed.returncode == 0,
            message=str(object=completed.stderr),
        )
        _require(
            condition=b"Executed 1 SML fixtures" in completed.stderr,
            message="The batch runner did not execute its fixture.",
        )
    _LOGGER.info(
        "SML cache controls passed with native compile and execution."
    )


if __name__ == "__main__":
    main()
