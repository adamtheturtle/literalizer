-module(fixture_literalize_ref_escaped_plain_string_erlang_ref).
-export([x/0]).
x() ->
    My_data = [
        0,
        [["plain"]]
    ],
    My_data.
