-module(fixture_scalar_int_very_large_erlang).
-export([x/0]).
x() ->
    My_data = 9223372036854775808,
    My_data.
