-module(fixture_float_scientific_notation_erlang).
-export([x/0]).
x() ->
    My_data = [
        0.0,
        1.0,
        1500.0,
        0.001,
        1.0e16
    ],
    My_data.
