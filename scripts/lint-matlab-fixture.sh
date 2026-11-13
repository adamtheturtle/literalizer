# Parse-check one Matlab fixture under Octave, preserving the skips
# documented at the `Lint Matlab` step in `.github/workflows/lint.yml`.
#
# Octave is a practical CI substitute for MATLAB but does not support
# every MATLAB builtin, so two fixture classes are skipped:
#   - files containing `""` (MATLAB-escaped double quotes): Octave
#     accepts some backslash escapes (e.g. `\"`) that MATLAB rejects,
#     so the parse check would be misleading.
#   - files using the `datetime` builtin: not implemented in Octave.
#   - `containers.Map` fixtures with empty character-array keys: MATLAB
#     accepts these keys, while Octave rejects them in `cell2struct`.
#
# Invoked through `bash` (see the `Lint Matlab` workflow step), so no
# shebang or execute bit is needed here.
set -euo pipefail

f="$1"

if grep -q '""' "$f"; then
    echo "Skipping Octave parse check for MATLAB-escaped quotes in $f"
    exit 0
fi

if grep -qw datetime "$f"; then
    echo "Skipping $f — uses datetime(), which Octave does not implement"
    exit 0
fi

if grep -q "containers.Map({''" "$f"; then
    echo "Skipping $f — Octave rejects MATLAB's empty containers.Map key"
    exit 0
fi

# Versioned golden filenames contain @, which makes Octave treat a
# function file as a script. Give complete function consumers their
# declared entry-point filename, as the other native compiler hosts do.
first_line=$(sed -n '/^[[:space:]]*$/d; /^[[:space:]]*%/d; {p;q;}' "$f")
octave_args=("$f")
if [[ $first_line =~ ^[[:space:]]*function[[:space:]]+([[:alpha:]][[:alnum:]_]*)[[:space:]]*\( ]]; then
    workspace=$(mktemp -d)
    trap 'rm -rf "$workspace"' EXIT
    entrypoint="${BASH_REMATCH[1]}"
    cp "$f" "$workspace/$entrypoint.m"
    octave_args=(--path "$workspace" --eval "$entrypoint()")
fi

scripts/run-bounded.sh "$f" --signal=KILL 60s octave --norc --no-gui "${octave_args[@]}"
