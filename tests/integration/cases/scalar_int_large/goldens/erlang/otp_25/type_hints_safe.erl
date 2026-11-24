-module(fixture_scalar_int_large_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = 2147483648,
    My_data.
