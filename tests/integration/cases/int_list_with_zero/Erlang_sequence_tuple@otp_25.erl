-module(fixture_int_list_with_zero_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        0,
        1,
        -1
    },
    My_data.
