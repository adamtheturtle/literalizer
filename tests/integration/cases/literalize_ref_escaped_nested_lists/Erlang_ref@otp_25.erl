-module(fixture_literalize_ref_escaped_nested_lists_erlang_ref).
-export([x/0]).
x() ->
    Existing = 1,
    My_data = [
        0,
        [[Existing]]
    ],
    My_data.
