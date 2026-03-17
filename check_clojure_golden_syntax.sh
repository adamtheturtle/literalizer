#!/bin/bash
# Check syntax of Clojure golden files using clj-kondo, if available

if ! command -v clj-kondo &> /dev/null; then
    exit 0
fi

clj-kondo --lint "$@"
