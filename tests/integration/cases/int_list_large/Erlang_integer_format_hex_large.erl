-module(fixture_int_list_large_erlang_integer_format_hex_large).
-export([x/0]).
x() ->
    My_data = [
        16#F4240,
        -16#4D2,
        16#FF,
        -16#A
    ],
    My_data.
