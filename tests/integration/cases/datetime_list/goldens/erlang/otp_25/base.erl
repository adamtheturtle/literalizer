-module(fixture_datetime_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        "2024-01-15T12:30:00.123456+00:00",
        "2024-06-01T08:00:00+00:00"
    ],
    My_data.
