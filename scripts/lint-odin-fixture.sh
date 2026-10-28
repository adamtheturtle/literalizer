#!/usr/bin/env bash

set -euo pipefail

source_path=$(realpath "$1")
bounded_runner=$(realpath "$(dirname "$0")/run-bounded.sh")
workspace=$(mktemp -d)
trap 'rm -rf "$workspace"' EXIT
cp "$source_path" "$workspace/main.odin"

# Odin reports linker calls and the generated-program launch before running
# them. Keep the compiler and runtime inside the same attempt budget.
# One internal worker avoids the pinned compiler's parallel LLVM crashes
# tracked in issue 6298; retain it until a released compiler passes validation.
printf 'Compiling and running %s\n' "$source_path"
(
    cd "$workspace"
    "$bounded_runner" "$source_path" --kill-after=10s 60s \
        odin run . -thread-count:1 -out:"$workspace/prog" -show-system-calls
) || {
    status=$?
    printf 'Odin attempt failed (exit %s): %s\n' "$status" "$source_path" >&2
    exit "$status"
}
