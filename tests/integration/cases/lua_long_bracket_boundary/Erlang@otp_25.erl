-module(fixture_lua_long_bracket_boundary_erlang).
-export([x/0]).
x() ->
    My_data = [
        "]",
        "a]",
        "a]=",
        "a]b"
    ],
    My_data.
