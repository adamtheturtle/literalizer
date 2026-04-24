# Parse-check one Matlab fixture under Octave, preserving the skips
# documented at the `Lint Matlab` step in `.github/workflows/lint.yml`.
#
# Octave is a practical CI substitute for MATLAB but does not support
# every MATLAB builtin, so two fixture classes are skipped:
#   - files containing `""` (MATLAB-escaped double quotes): Octave
#     accepts some backslash escapes (e.g. `\"`) that MATLAB rejects,
#     so the parse check would be misleading.
#   - files using the `datetime` builtin: not implemented in Octave.
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

octave --norc --no-gui "$f"
