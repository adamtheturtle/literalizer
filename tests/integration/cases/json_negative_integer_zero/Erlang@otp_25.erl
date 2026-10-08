-module(fixture_json_negative_integer_zero_erlang).
-export([x/0]).
x() ->
    My_data = -0.0,
    My_data.
