#!/usr/bin/env bash

set -euo pipefail

fixture=$1
bounded_runner=$(realpath "$(dirname "$0")/run-bounded.sh")
workspace=$(mktemp -d)
trap 'rm -rf "$workspace"' EXIT

# Keep each compiler/runtime attempt bounded, including termination of its
# descendants. GNU time records the whole attempt, even when timeout kills
# the compiler. Labels bracket successful attempts as well as failures so
# interleaved parallel output identifies every active fixture.
printf '%s: START %s (pid %s)\n' "$fixture" "$(date -u +%FT%TZ)" "$$" >&2
status=0
/usr/bin/time --quiet -o "$workspace/resources" \
    -f 'elapsed=%es max_rss=%MKiB exit=%x' \
    "$bounded_runner" "$fixture" --signal=KILL 60s \
    mojo run --num-threads 1 --Werror "$fixture" > "$workspace/output" 2>&1 || status=$?
# Emit completed diagnostics together. Otherwise even a single GNU time
# line can interleave byte-by-byte with another compiler's output.
{
    flock 9
    printf '::group::%s\n' "$fixture"
    cat "$workspace/output"
    printf '%s: END %s (status %s; %s)\n' \
        "$fixture" "$(date -u +%FT%TZ)" "$status" "$(cat "$workspace/resources")"
    printf '::endgroup::\n'
} 9> "${RUNNER_TEMP:-/tmp}/literalizer-mojo-output.lock" >&2
# xargs stops consuming input on exit 255. Preserve the actual status in
# diagnostics while letting every remaining fixture finish after a failure.
if ((status != 0)); then
    exit 1
fi
