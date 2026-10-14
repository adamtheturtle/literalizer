-module(fixture_elm_signed_constructor_arguments_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        -42,
        0,
        42,
        -1.250000,
        0.000000,
        1.250000
    ],
    My_data.
