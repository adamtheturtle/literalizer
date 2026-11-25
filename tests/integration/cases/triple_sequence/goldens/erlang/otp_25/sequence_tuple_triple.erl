-module(fixture_triple_sequence_erlang_sequence_tuple_triple).
-export([x/0]).
x() ->
    My_data = {
        1,
        "hello",
        true
    },
    My_data.
