#!/usr/bin/env bash

# Download a pinned artifact, trying the supplied sources in order. Publish
# it only after its SHA-256 matches; never replace an existing file on failure.
set -euo pipefail

expected_sha256=$1
destination=$2
shift 2

temporary=$(mktemp "${destination}.XXXXXX")
trap 'rm -f "$temporary"' EXIT

for url in "$@"; do
    # A last attempt can start just before the retry window ends: each
    # source therefore takes at most 45 + 30 seconds. Two sources for
    # each of three Jackson jars fit inside the 10-minute setup step.
    if curl --fail --show-error --silent --location \
        --retry 2 --retry-all-errors --retry-max-time 45 \
        --connect-timeout 10 --max-time 30 \
        --write-out 'download HTTP %{http_code}: %{url_effective}\n' \
        "$url" --output "$temporary"; then
        if ! printf '%s  %s\n' "$expected_sha256" "$temporary" |
            shasum --algorithm 256 --check --status; then
            echo "SHA-256 mismatch: $url" >&2
            exit 1
        fi
        mv "$temporary" "$destination"
        exit 0
    fi
    echo "download failed: $url" >&2
done

echo "all artifact sources failed: $destination" >&2
exit 1
