-module(fixture_scalar_int_negative_large_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = -2147483649,
    My_data.
