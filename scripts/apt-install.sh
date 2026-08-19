#!/usr/bin/env bash

# Install apt packages, abandoning a stalled mirror instead of waiting
# on it.
#
# A hung `apt-get` consumed the whole `timeout-minutes` budget of the
# lint job it ran in, which failed the completion gate and needed a
# manual re-run (issue #3982).  Each attempt is bounded by `timeout`,
# so a mirror that stops responding costs one attempt rather than the
# job.
#
# `timeout` runs under `sudo` rather than around it: an unprivileged
# `timeout` cannot signal a root `apt-get`, so its SIGTERM is refused
# and the bound never fires.  `--kill-after` follows up with SIGKILL so
# a wedged apt-get cannot hold its lock into the next attempt.

set -euo pipefail

attempts=3
attempt_seconds=180

for attempt in $(seq 1 "$attempts"); do
    if sudo timeout --kill-after=10 "$attempt_seconds" apt-get update &&
        sudo timeout --kill-after=10 "$attempt_seconds" apt-get install \
            -y "$@"; then
        exit 0
    fi
    echo "apt-get attempt $attempt of $attempts failed or timed out" >&2
    sleep 5
done

echo "apt-get failed after $attempts attempts: $*" >&2
exit 1
