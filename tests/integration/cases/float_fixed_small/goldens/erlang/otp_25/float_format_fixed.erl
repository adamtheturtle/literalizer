-module(fixture_float_fixed_small_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        0.000000001,
        -0.000000001
    ],
    My_data.
