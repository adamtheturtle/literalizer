-module(fixture_binary_list_erlang_sequence_tuple_binary).
-export([x/0]).
x() ->
    My_data = {
        <<72, 101, 108, 108, 111>>
    },
    My_data.
