#!/usr/bin/env bash

set -euo pipefail

mode=$1
fixture_path=$2

case "$fixture_path" in
*@cpp14.cpp) standard=c++14 ;;
*@cpp17.cpp) standard=c++17 ;;
*) standard=c++20 ;;
esac

case "$mode" in
tidy)
    clang-tidy "$fixture_path" -- "-std=$standard"
    ;;
run)
    temporary_directory=$(mktemp -d)
    trap 'rm -rf "$temporary_directory"' EXIT
    clang++ "-std=$standard" \
        -include-pch "/tmp/lint-cpp-$standard.hpp.pch" \
        "$fixture_path" \
        -o "$temporary_directory/run"
    "$temporary_directory/run"
    ;;
*)
    echo "Unknown C++ fixture lint mode: $mode" >&2
    exit 2
    ;;
esac
