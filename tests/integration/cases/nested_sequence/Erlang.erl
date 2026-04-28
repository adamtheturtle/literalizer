-module(fixture_nested_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        true,
        "hi",
        [1, 2],
        undefined
    ],
    My_data.
