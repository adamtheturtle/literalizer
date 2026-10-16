-module(fixture_nested_sequence_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        true,
        "hi",
        {1, 2},
        undefined
    },
    My_data.
