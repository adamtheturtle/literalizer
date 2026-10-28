#!/usr/bin/env bash

# Keep setup-swift's key import, refresh retries and signature verification.
# Bound each GPG invocation and use HTTPS for its Ubuntu keyserver requests.
set -euo pipefail

arguments=("$@")
for ((index = 1; index < ${#arguments[@]}; index++)); do
    if [[ ${arguments[index - 1]} == --keyserver &&
        ${arguments[index]} == hkp://keyserver.ubuntu.com ]]; then
        arguments[index]=hkps://keyserver.ubuntu.com:443
    fi
done

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
exec "$script_dir/run-bounded.sh" 'Swift GPG' --kill-after=10s 60s \
    "${SWIFT_SETUP_GPG:?The original GPG executable must be set}" "${arguments[@]}"
