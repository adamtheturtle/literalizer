-module(fixture_nested_singleton_sequence_root_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[[[[[[1]]]]]]]
    ],
    My_data.
