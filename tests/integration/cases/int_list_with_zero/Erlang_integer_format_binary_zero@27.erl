-module(fixture_int_list_with_zero_erlang_integer_format_binary_zero).
-export([x/0]).
x() ->
    My_data = [
        2#0,
        2#1,
        -2#1
    ],
    My_data.
