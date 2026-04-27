-module(fixture_simple_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        "hello",
        true,
        undefined
    ],
    My_data.
