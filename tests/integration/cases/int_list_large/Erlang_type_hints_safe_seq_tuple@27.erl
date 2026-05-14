-module(fixture_int_list_large_erlang_type_hints_safe_seq_tuple).
-export([x/0]).
x() ->
    My_data = {
        1000000,
        -1234,
        255,
        -10
    },
    My_data.
