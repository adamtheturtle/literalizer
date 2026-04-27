-module(fixture_int_list_with_zero_erlang_integer_format_hex_zero).
-export([x/0]).
x() ->
    My_data = [
        16#0,
        16#1,
        -16#1
    ],
    My_data.
