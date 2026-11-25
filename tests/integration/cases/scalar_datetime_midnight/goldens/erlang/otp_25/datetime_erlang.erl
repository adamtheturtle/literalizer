-module(fixture_scalar_datetime_midnight_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = {{2024, 1, 15}, {0, 0, 0}},
    My_data.
