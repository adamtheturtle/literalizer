-module(fixture_nested_list_mixed_sibling_types_erlang).
-export([x/0]).
x() ->
    My_data = [
        [1, 2],
        [],
        ["a", "b"]
    ],
    My_data.
