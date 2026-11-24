-module(fixture_multiline_raw_string_delimiter_erlang).
-export([x/0]).
x() ->
    My_data = [
        "custom base after empty collision: )\"\nvalue",
        "custom suffix after base collision: )\" and )x0\"\nvalue",
        "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
        "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
    ],
    My_data.
