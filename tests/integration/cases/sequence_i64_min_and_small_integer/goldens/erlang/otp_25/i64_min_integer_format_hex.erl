-module(fixture_sequence_i64_min_and_small_integer_erlang_i64_min_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        -16#8000000000000000,
        16#1
    ],
    My_data.
