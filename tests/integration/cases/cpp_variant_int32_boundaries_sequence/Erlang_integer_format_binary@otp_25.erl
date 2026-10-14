-module(fixture_cpp_variant_int32_boundaries_sequence_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        -2#10000000000000000000000000000000,
        -2#1111111111111111111111111111111,
        [2#0]
    ],
    My_data.
