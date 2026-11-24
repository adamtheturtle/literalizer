-module(fixture_yaml_negative_integer_zero_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = -0.0,
    My_data.
