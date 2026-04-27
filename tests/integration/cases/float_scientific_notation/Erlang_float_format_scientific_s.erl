-module(fixture_float_scientific_notation_erlang_float_format_scientific_s).
-export([x/0]).
x() ->
    My_data = [
        0.0,
        1.0,
        1.5e3,
        1.0e-3
    ],
    My_data.
