-module(fixture_float_negative_zero_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        -0.000000,
        1.500000
    ],
    My_data.
