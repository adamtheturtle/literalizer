-module(fixture_scalar_null_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = undefined,
    My_data.
