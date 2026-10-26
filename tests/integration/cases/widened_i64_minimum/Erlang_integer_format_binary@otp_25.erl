-module(fixture_widened_i64_minimum_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        -2#1000000000000000000000000000000000000000000000000000000000000000,
        2#101
    ],
    My_data.
