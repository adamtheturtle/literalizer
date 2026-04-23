"""Shared helpers for the Elm lint scripts."""

import json

ELM_JSON = json.dumps(
    obj={
        "type": "application",
        "source-directories": ["src"],
        "elm-version": "0.19.1",
        "dependencies": {
            "direct": {"elm/core": "1.0.5"},
            "indirect": {"elm/json": "1.1.3"},
        },
        "test-dependencies": {"direct": {}, "indirect": {}},
    },
)
