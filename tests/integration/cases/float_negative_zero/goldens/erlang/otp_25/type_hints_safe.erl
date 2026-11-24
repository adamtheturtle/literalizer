-module(fixture_float_negative_zero_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        -0.0,
        1.5
    ],
    My_data.
