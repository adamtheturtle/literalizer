-module(fixture_negative_zero_constructor_arguments_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = [
        -0.0,
        0.0
    ],
    My_data.
