#!/usr/bin/env bash

# Usage: run-bounded.sh LABEL [TIMEOUT_OPTION ...] DURATION COMMAND [ARG ...]
# Pass GNU timeout's options and command unchanged; this helper only
# discovers timeout/gtimeout and adds fixture-labelled diagnostics.
# Diagnostics go to stderr so stdin/stdout remain the command's streams.
set -euo pipefail

if (($# < 3)); then
    echo 'Usage: run-bounded.sh LABEL [TIMEOUT_OPTION ...] DURATION COMMAND [ARG ...]' >&2
    exit 2
fi
label=$1
shift

if command -v timeout > /dev/null 2>&1; then
    timeout_command=timeout
elif command -v gtimeout > /dev/null 2>&1; then
    timeout_command=gtimeout
else
    echo 'GNU timeout is required; install coreutils (gtimeout on macOS).' >&2
    exit 127
fi

printf '%s: running:' "$label" >&2
printf ' %q' "$timeout_command" --verbose "$@" >&2
printf '\n' >&2
SECONDS=0
if "$timeout_command" --verbose "$@"; then
    exit 0
else
    status=$?
    printf '%s: command failed (status %s; elapsed %ss):' \
        "$label" "$status" "$SECONDS" >&2
    printf ' %q' "$timeout_command" --verbose "$@" >&2
    printf '\n' >&2
    exit "$status"
fi
