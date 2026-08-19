#!/usr/bin/env bash

# Install apt packages, abandoning a stalled mirror instead of waiting
# on it.
#
# A hung `apt-get` consumed the whole `timeout-minutes` budget of the
# lint job it ran in, which failed the completion gate and needed a
# manual re-run (issue #3982).  Each attempt is bounded by `timeout`,
# so a mirror that stops responding costs one attempt rather than the
# job.

set -euo pipefail

attempts=3
attempt_seconds=180

for attempt in $(seq 1 "$attempts"); do
    if timeout "$attempt_seconds" sudo apt-get update &&
        timeout "$attempt_seconds" sudo apt-get install -y "$@"; then
        exit 0
    fi
    echo "apt-get attempt $attempt of $attempts failed or timed out" >&2
    sleep 5
done

echo "apt-get failed after $attempts attempts: $*" >&2
exit 1
