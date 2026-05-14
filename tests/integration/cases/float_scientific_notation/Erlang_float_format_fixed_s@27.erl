-module(fixture_float_scientific_notation_erlang_float_format_fixed_s).
-export([x/0]).
x() ->
    My_data = [
        0.000000,
        1.000000,
        1500.000000,
        0.001000
    ],
    My_data.
