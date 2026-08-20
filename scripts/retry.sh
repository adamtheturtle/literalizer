#!/usr/bin/env bash

# Run one network install command, abandoning a stalled or failing
# attempt instead of waiting on it.
#
# A hung `apt-get` consumed the whole `timeout-minutes` budget of the
# lint job it ran in, which failed the completion gate and needed a
# manual re-run; a `cabal update` against a slow index fails the same
# way (issue #3982).  Each attempt is bounded by `timeout`, so a
# registry that stops responding costs one attempt rather than a job.
#
# A `sudo` command takes the timeout inside the `sudo`: an unprivileged
# `timeout` cannot signal a root child, so its SIGTERM is refused and
# the bound never fires.  `--kill-after` follows up with SIGKILL so a
# wedged process cannot hold a lock into the next attempt.

set -euo pipefail

attempts=3
attempt_seconds=300

if [[ ${1:-} == sudo ]]; then
    shift
    bounded=(sudo timeout --kill-after=10 "$attempt_seconds")
else
    bounded=(timeout --kill-after=10 "$attempt_seconds")
fi

for attempt in $(seq 1 "$attempts"); do
    if "${bounded[@]}" "$@"; then
        exit 0
    fi
    echo "attempt $attempt of $attempts failed or timed out: $*" >&2
    sleep 5
done

echo "failed after $attempts attempts: $*" >&2
exit 1
