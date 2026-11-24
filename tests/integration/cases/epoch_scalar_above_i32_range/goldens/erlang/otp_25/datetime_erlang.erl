-module(fixture_epoch_scalar_above_i32_range_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = {{2099, 6, 15}, {8, 30, 0}},
    My_data.
