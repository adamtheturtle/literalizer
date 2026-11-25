-module(fixture_string_with_backslash_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = [
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline"
    ],
    My_data.
