-module(fixture_scalar_datetime_erlang_type_hints_safe_dt_erlang).
-export([x/0]).
x() ->
    My_data = {{2024, 1, 15}, {12, 30, 0}},
    My_data.
