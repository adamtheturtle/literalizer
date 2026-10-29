-module(fixture_closing_bracket_string_boundaries_erlang).
-export([x/0]).
x() ->
    My_data = [
        "]",
        "a]",
        "a]=",
        "a]b"
    ],
    My_data.
