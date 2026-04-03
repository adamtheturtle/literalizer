-module(check).
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
