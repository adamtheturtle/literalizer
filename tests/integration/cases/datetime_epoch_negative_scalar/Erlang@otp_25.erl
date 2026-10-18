-module(fixture_datetime_epoch_negative_scalar_erlang).
-export([x/0]).
x() ->
    My_data = "1969-12-31T23:59:59+00:00",
    My_data.
