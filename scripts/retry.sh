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

# Two calls share one step's ``timeout-minutes: 10`` (600s) budget in
# every job that uses this helper, so one call must fit inside 300s:
#
#     attempts x (attempt_seconds + kill_after) + (attempts - 1) x backoff
#     3 x (80 + 10) + 2 x 5 = 280s
#
# Sized so every configured attempt is reachable.  With the previous
# 300s the arithmetic came to 945s per call, so the step timeout killed
# the run part-way through attempt 2, attempt 3 never ran, and the
# second command in the step never started at all (issue #3982).
attempts=3
attempt_seconds=80
backoff_seconds=5

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
    # No backoff after the final attempt: waiting before giving up buys
    # nothing and spends budget the next call in the step needs.
    if ((attempt < attempts)); then
        sleep "$backoff_seconds"
    fi
done

echo "failed after $attempts attempts: $*" >&2
exit 1
