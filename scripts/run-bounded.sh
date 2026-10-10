#!/usr/bin/env bash

# Usage: run-bounded.sh LABEL DEADLINE KILL_AFTER COMMAND [ARG ...]
# Durations use GNU timeout syntax (e.g. 60s). KILL_AFTER=KILL kills the
# process group immediately; a duration sends TERM followed by KILL.
# Diagnostics go to stderr so stdin/stdout remain the command's streams.
set -euo pipefail

if (($# < 4)); then
    echo 'Usage: run-bounded.sh LABEL DEADLINE KILL_AFTER COMMAND [ARG ...]' >&2
    exit 2
fi
label=$1
deadline=$2
kill_after=$3
shift 3

if command -v timeout > /dev/null 2>&1; then
    timeout_command=timeout
elif command -v gtimeout > /dev/null 2>&1; then
    timeout_command=gtimeout
else
    echo 'GNU timeout is required; install coreutils (gtimeout on macOS).' >&2
    exit 127
fi

if [[ $kill_after == KILL ]]; then
    termination=(--signal=KILL)
else
    termination=(--kill-after="$kill_after")
fi

printf '%s: running (deadline %s):' "$label" "$deadline" >&2
printf ' %q' "$@" >&2
printf '\n' >&2
SECONDS=0
if "$timeout_command" --verbose "${termination[@]}" "$deadline" "$@"; then
    exit 0
else
    status=$?
    printf '%s: command failed (status %s; deadline %s; elapsed %ss):' \
        "$label" "$status" "$deadline" "$SECONDS" >&2
    printf ' %q' "$@" >&2
    printf '\n' >&2
    exit "$status"
fi
