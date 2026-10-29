-module(fixture_epoch_scalar_below_i32_range_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = -2147483649,
    My_data.
