-module(fixture_negative_zero_constructor_arguments_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        -0.000000,
        0.000000
    ],
    My_data.
