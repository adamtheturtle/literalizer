-module(fixture_scalar_datetime_non_utc_erlang_datetime_erlang_non_utc).
-export([x/0]).
x() ->
    My_data = {{2024, 1, 15}, {18, 0, 0}},
    My_data.
