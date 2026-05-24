r"""Perl JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Perl
``my $myData = ...;`` declaration, wrap it in a tiny script that prints
``JSON::PP->new->utf8->allow_bignum->encode($myData)``, run it with
Perl, and hand the emitted JSON to :func:`roundtrip_common.verify`.

Three non-default Perl options are used so the round-trip is faithful
for the values Perl *can* represent:

* ``bool_format=JSON_PP_REF`` renders booleans as ``\1`` / ``\0``,
  which ``JSON::PP`` encodes as JSON ``true`` / ``false``.  The default
  ``INTEGER`` form would collapse booleans to the integers ``1`` / ``0``
  (see issue #2586).
* ``integer_width_strategy=MATH_BIG_INT`` renders integers wider than a
  native scalar via ``Math::BigInt->new("...")``, which the ``JSON::PP``
  ``allow_bignum`` mode then serializes back as a plain JSON integer.
  The default ``BARE`` form would silently demote the 26-digit
  ``biginteger`` field to an NV (see issue #2588).
* ``float_format=MATH_BIG_FLOAT`` wraps every float as
  ``Math::BigFloat->new("...")``, which ``allow_bignum`` then
  serializes back with full precision.  The default ``REPR`` form is
  re-encoded by ``JSON::PP`` / ``JSON::XS`` with their hard-coded
  15-digit ``%.15g`` precision, which rounds ``DBL_MAX``
  (``float_large_exponent = 1.7976931348623157e+308``) up past
  ``DBL_MAX`` and Python decodes the result as ``inf`` (see issue
  #2605).

``double_array`` (``[1.0, 2.5]`` -> ``[1, 2.5]``) and ``negative_zero``
(``-0.0`` -> ``0``) survive the comparison because Python treats
``1.0 == 1`` and ``-0.0 == 0`` as equal, so they do not need to be
excluded even though Perl scalars discard the distinction.

This lives here, driven by the ``Perl roundtrip`` step of the
``lint-perl`` job in ``.github/workflows/lint.yml``, because that job is
where the pinned Perl toolchain is installed.  It shares the same input
and comparison logic as the other per-language round-trip helpers.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Perl

_VAR_NAME = "myData"
_LABEL = "Perl"
_EXCLUDED_KEYS: tuple[str, ...] = ()


def _build_program(json_text: str) -> str:
    """Return a runnable Perl program literalized from *json_text*."""
    language = Perl(
        bool_format=Perl.bool_formats.JSON_PP_REF,
        integer_width_strategy=Perl.integer_width_strategies.MATH_BIG_INT,
        float_format=Perl.float_formats.MATH_BIG_FLOAT,
    )
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "use strict;\n"
        "use warnings;\n"
        "use JSON::PP;\n"
        f"{preamble}\n"
        f"{result.code}\n"
        "my $json = JSON::PP->new->utf8->allow_bignum->canonical;\n"
        "binmode STDOUT;\n"
        f"print $json->encode(${_VAR_NAME});\n"
    )


def main() -> None:
    """Round-trip the shared document through the Perl backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    perl = shutil.which(cmd="perl") or "perl"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        script_path = Path(tmpdir_name) / "main.pl"
        script_path.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[perl, str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: perl runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
