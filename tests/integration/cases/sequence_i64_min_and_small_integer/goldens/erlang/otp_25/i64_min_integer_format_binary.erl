-module(fixture_sequence_i64_min_and_small_integer_erlang_i64_min_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        -2#1000000000000000000000000000000000000000000000000000000000000000,
        2#1
    ],
    My_data.
