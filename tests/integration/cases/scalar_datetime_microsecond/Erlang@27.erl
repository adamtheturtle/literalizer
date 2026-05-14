-module(fixture_scalar_datetime_microsecond_erlang).
-export([x/0]).
x() ->
    My_data = "2024-01-15T12:30:00.123456+00:00",
    My_data.
