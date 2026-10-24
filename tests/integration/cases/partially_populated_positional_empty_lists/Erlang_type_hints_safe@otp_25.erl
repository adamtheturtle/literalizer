-module(fixture_partially_populated_positional_empty_lists_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [[], []],
        [[], [1]]
    ],
    My_data.
