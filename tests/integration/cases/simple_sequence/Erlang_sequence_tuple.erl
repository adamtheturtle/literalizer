-module(fixture_simple_sequence_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        1,
        "hello",
        true,
        undefined
    },
    My_data.
