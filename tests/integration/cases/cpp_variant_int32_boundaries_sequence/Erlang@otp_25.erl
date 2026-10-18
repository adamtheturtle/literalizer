-module(fixture_cpp_variant_int32_boundaries_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        -2147483648,
        -2147483647,
        [0]
    ],
    My_data.
