-module(fixture_pair_sequence_erlang_sequence_tuple_pair).
-export([x/0]).
x() ->
    My_data = {
        1,
        "hello"
    },
    My_data.
