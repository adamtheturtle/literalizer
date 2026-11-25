#!/usr/bin/env bash

set -euo pipefail

mode=$1
fixture_path=$2

case "$fixture_path" in
*/goldens/cpp/cpp14/*.cpp) standard=c++14 ;;
*/goldens/cpp/cpp17/*.cpp) standard=c++17 ;;
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
    # Require direct C++ includes in addition to the shared checks.
    scripts/run-bounded.sh "$fixture_path" --signal=KILL 60s \
        clang-tidy --checks=misc-include-cleaner "$fixture_path" -- "-std=$standard"
    ;;
run)
    temporary_directory=$(mktemp -d)
    trap 'rm -rf "$temporary_directory"' EXIT
    source_path=$fixture_path
    case "$fixture_path" in
    */goldens/cpp/*/default_module_name.cpp)
        # Exercise the public default Module() through caller-owned main().
        # Keep the generated source bytes and identifiers unchanged.
        cp "$fixture_path" "$temporary_directory/module.cpp"
        printf '#include "module.cpp"\nint main() { return Module(); }\n' \
            > "$temporary_directory/check.cpp"
        source_path=$temporary_directory/check.cpp
        ;;
    esac
    scripts/run-bounded.sh "$fixture_path" --signal=KILL 60s \
        clang++ "-std=$standard" -Werror \
        "$source_path" \
        -o "$temporary_directory/run"
    scripts/run-bounded.sh "$fixture_path" --signal=KILL 60s \
        "$temporary_directory/run"
    ;;
*)
    echo "Unknown C++ fixture lint mode: $mode" >&2
    exit 2
    ;;
esac
