-module(fixture_json5_negative_integer_zero_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = -0.000000,
    My_data.
