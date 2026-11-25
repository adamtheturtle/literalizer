-module(fixture_float_fixed_small_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = [
        1.0e-9,
        -1.0e-9
    ],
    My_data.
