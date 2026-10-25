-module(fixture_four_dimensional_empty_lists_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [[[]]],
        [[[]]]
    ],
    My_data.
