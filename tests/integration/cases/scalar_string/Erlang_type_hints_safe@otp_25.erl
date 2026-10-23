-module(fixture_scalar_string_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = "hello",
    My_data.
