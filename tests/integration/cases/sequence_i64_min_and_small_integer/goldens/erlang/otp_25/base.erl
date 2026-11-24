-module(fixture_sequence_i64_min_and_small_integer_erlang).
-export([x/0]).
x() ->
    My_data = [
        -9223372036854775808,
        1
    ],
    My_data.
