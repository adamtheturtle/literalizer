-module(fixture_datetime_and_integer_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        "2000-01-01T01:02:03",
        1
    ],
    My_data.
