-module(fixture_int_list_with_zero_erlang).
-export([x/0]).
x() ->
    My_data = [
        0,
        1,
        -1
    ],
    My_data.
