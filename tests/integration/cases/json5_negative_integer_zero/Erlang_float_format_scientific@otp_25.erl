-module(fixture_json5_negative_integer_zero_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = -0.0,
    My_data.
