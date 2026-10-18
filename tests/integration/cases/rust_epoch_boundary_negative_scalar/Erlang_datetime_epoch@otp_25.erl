-module(fixture_rust_epoch_boundary_negative_scalar_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = -2147483649,
    My_data.
