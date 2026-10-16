#!/usr/bin/env bash

set -euo pipefail

if [[ ${1:-} == --pool ]]; then
    cgroup_path=$(sed -n 's/^0:://p' /proc/self/cgroup)
    resource_root="/sys/fs/cgroup$cgroup_path"
    # Verify the actual controller ceiling before launching any compiler.
    test "$(cat "$resource_root/memory.max")" = 4294967296
    for resource in memory.high memory.max memory.swap.max; do
        printf 'Mojo pool %s=%s\n' "$resource" "$(cat "$resource_root/$resource")"
    done
    status=0
    xargs -0 -P 2 -n1 scripts/lint-mojo-fixture.sh || status=$?
    printf 'Mojo pool memory.peak=%s\n' "$(cat "$resource_root/memory.peak")"
    printf 'Mojo pool memory.events:\n'
    cat "$resource_root/memory.events"
    exit "$status"
fi

# Keep a runaway compiler inside its own memory controller rather than
# competing with the Actions runner. Pressure starts at 3 GiB; the whole
# two-worker pool has a hard 4 GiB ceiling and cannot consume swap.
# Drop back to the invoking user before executing fixture programs.
exec sudo -n systemd-run --scope --quiet \
    --property=MemoryHigh=3G --property=MemoryMax=4G --property=MemorySwapMax=0 \
    setpriv --reuid="$(id -u)" --regid="$(id -g)" --init-groups \
    env "HOME=$HOME" "PATH=$PATH" "RUNNER_TEMP=${RUNNER_TEMP:-/tmp}" \
    "RUNNER_TRACKING_ID=${RUNNER_TRACKING_ID:-}" \
    bash "$0" --pool
