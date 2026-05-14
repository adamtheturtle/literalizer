-module(fixture_int_list_large_erlang_integer_format_binary_large).
-export([x/0]).
x() ->
    My_data = [
        2#11110100001001000000,
        -2#10011010010,
        2#11111111,
        -2#1010
    ],
    My_data.
