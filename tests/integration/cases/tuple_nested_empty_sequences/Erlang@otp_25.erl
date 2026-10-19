-module(fixture_tuple_nested_empty_sequences_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1, "value"], []]
    ],
    My_data.
