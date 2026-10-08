-module(fixture_nim_non_decimal_i64_min_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        -16#8000000000000000,
        -16#1,
        16#7FFFFFFFFFFFFFFF
    ],
    My_data.
