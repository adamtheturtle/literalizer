-module(fixture_rust_epoch_boundary_negative_scalar_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = {{1901, 12, 13}, {20, 45, 51}},
    My_data.
