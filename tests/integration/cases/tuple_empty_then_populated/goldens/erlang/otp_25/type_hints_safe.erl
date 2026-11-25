-module(fixture_tuple_empty_then_populated_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [1, []],
        [2, [3]]
    ],
    My_data.
