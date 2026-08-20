#!/usr/bin/env bash

# Run one network install command, abandoning a stalled or failing
# attempt instead of waiting on it.
#
# A hung `apt-get` consumed the whole `timeout-minutes` budget of the
# lint job it ran in, which failed the completion gate and needed a
# manual re-run; a `cabal update` against a slow index fails the same
# way (issue #3982).  Each attempt is bounded by `timeout`, so a
# registry that stops responding costs one attempt rather than a job.

set -euo pipefail

attempts=3
attempt_seconds=300

for attempt in $(seq 1 "$attempts"); do
    if timeout "$attempt_seconds" "$@"; then
        exit 0
    fi
    echo "attempt $attempt of $attempts failed or timed out: $*" >&2
    sleep 5
done

echo "failed after $attempts attempts: $*" >&2
exit 1
