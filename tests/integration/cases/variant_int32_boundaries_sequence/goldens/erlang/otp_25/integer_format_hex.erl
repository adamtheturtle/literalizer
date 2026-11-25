-module(fixture_variant_int32_boundaries_sequence_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        -16#80000000,
        -16#7FFFFFFF,
        [16#0]
    ],
    My_data.
