-module(fixture_int_list_with_zero_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        0,
        1,
        -1
    ],
    My_data.
