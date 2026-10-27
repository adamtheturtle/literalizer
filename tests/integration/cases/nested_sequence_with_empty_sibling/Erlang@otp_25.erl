-module(fixture_nested_sequence_with_empty_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1]],
        [[]]
    ],
    My_data.
