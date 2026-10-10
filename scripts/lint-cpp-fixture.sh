#!/usr/bin/env bash

set -euo pipefail

mode=$1
fixture_path=$2

case "$fixture_path" in
*@cpp14.cpp) standard=c++14 ;;
*@cpp17.cpp) standard=c++17 ;;
*) standard=c++20 ;;
esac

# Some cross-format fixtures retain their versioned filename while an
# explicitly selected format requires a newer C++ library or syntax.
# Compile them with the minimum standard required by their generated code.
if grep -qE '^[[:space:]]*\.[[:alpha:]_][[:alnum:]_]*[[:space:]]*=' "$fixture_path" ||
    grep -qF 'std::chrono::year_month_day' "$fixture_path" ||
    grep -qF 'auto...' "$fixture_path"; then
    standard=c++20
elif [ "$standard" = c++14 ] && grep -qF 'std::variant' "$fixture_path"; then
    standard=c++17
fi

case "$mode" in
tidy)
    scripts/run-bounded.sh "$fixture_path" 60s KILL \
        clang-tidy "$fixture_path" -- "-std=$standard"
    ;;
run)
    temporary_directory=$(mktemp -d)
    trap 'rm -rf "$temporary_directory"' EXIT
    scripts/run-bounded.sh "$fixture_path" 60s KILL \
        clang++ "-std=$standard" \
        -include-pch "/tmp/lint-cpp-$standard.hpp.pch" \
        "$fixture_path" \
        -o "$temporary_directory/run"
    scripts/run-bounded.sh "$fixture_path" 60s KILL \
        "$temporary_directory/run"
    ;;
*)
    echo "Unknown C++ fixture lint mode: $mode" >&2
    exit 2
    ;;
esac
