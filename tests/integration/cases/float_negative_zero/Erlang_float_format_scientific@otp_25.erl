-module(fixture_float_negative_zero_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = [
        -0.0,
        1.5
    ],
    My_data.
