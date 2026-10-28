#!/usr/bin/env bash

# Check forwarding and failures without contacting a keyserver.
set -euo pipefail

workspace=$(mktemp -d)
trap 'rm -rf "$workspace"' EXIT

cat > "$workspace/gpg" << 'GPG'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$SWIFT_GPG_ARGUMENTS"
exit "${SWIFT_GPG_EXIT_STATUS:-0}"
GPG
chmod +x "$workspace/gpg"
export SWIFT_SETUP_GPG="$workspace/gpg"
export SWIFT_GPG_ARGUMENTS="$workspace/arguments"

scripts/swift-gpg.sh --keyserver hkp://keyserver.ubuntu.com --refresh-keys Swift
printf '%s\n' --keyserver hkps://keyserver.ubuntu.com:443 --refresh-keys Swift |
    cmp - "$SWIFT_GPG_ARGUMENTS"

scripts/swift-gpg.sh --verify 'signature with spaces.asc' 'archive with spaces.tar.gz'
printf '%s\n' --verify 'signature with spaces.asc' 'archive with spaces.tar.gz' |
    cmp - "$SWIFT_GPG_ARGUMENTS"

export SWIFT_GPG_EXIT_STATUS=17
if scripts/swift-gpg.sh --verify bad.asc archive.tar.gz; then
    echo 'A failed signature verification must remain a failure.' >&2
    exit 1
else
    status=$?
    test "$status" -eq 17
fi
