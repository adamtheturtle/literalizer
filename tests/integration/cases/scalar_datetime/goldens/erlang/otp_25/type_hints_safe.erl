-module(fixture_scalar_datetime_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = "2024-01-15T12:30:00+00:00",
    My_data.
