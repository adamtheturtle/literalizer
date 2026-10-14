#!/usr/bin/env bash

set -euo pipefail

source_path=$(realpath "$1")
workspace=$(mktemp -d)
trap 'rm -rf "$workspace"' EXIT
cp "$source_path" "$workspace/main.odin"

# Odin reports linker calls and the generated-program launch before running
# them. Keep the existing command and shared compiler/runtime attempt budget.
printf 'Compiling and running %s\n' "$source_path"
(
    cd "$workspace"
    timeout --verbose --kill-after=10s 60s \
        odin run . -out:"$workspace/prog" -show-system-calls
) || {
    status=$?
    printf 'Odin attempt failed (exit %s): %s\n' "$status" "$source_path" >&2
    exit "$status"
}
