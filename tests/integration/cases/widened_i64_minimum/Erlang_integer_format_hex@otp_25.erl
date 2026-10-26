-module(fixture_widened_i64_minimum_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        -16#8000000000000000,
        16#5
    ],
    My_data.
