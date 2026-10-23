-module(fixture_scalar_datetime_non_utc_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = "2024-01-15T18:00:00+05:30",
    My_data.
