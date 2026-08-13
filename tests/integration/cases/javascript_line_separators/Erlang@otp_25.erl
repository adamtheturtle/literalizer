-module(fixture_javascript_line_separators_erlang).
-export([x/0]).
x() ->
    My_data = [
        "a     b     c",
        "a\r     b"
    ],
    My_data.
