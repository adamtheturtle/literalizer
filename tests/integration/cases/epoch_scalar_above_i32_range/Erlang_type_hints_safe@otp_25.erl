-module(fixture_epoch_scalar_above_i32_range_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = "2099-06-15T08:30:00",
    My_data.
