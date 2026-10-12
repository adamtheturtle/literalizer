#!/usr/bin/env bash

# Download an artifact, trying the supplied sources in order.
# Replace the destination only after a successful download.
set -euo pipefail

destination=$1
shift

temporary=$(mktemp "${destination}.XXXXXX")
trap 'rm -f "$temporary"' EXIT

for url in "$@"; do
    # A last attempt can start just before the retry window ends: each
    # source therefore takes at most 45 + 30 seconds.
    printf 'download %s\n' "$url"
    if curl --fail --show-error --silent --location \
        --retry 2 --retry-all-errors --retry-max-time 45 \
        --connect-timeout 10 --max-time 30 \
        --write-out 'download HTTP %{http_code}\n' \
        "$url" --output "$temporary"; then
        mv "$temporary" "$destination"
        exit 0
    fi
    echo "download failed: $url" >&2
done

echo "all artifact sources failed: $destination" >&2
exit 1
