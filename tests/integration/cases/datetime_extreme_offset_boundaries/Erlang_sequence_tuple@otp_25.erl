-module(fixture_datetime_extreme_offset_boundaries_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        "2020-06-15T12:00:00-23:59",
        "2020-06-15T12:00:00-18:00",
        "2020-06-15T12:00:00+18:00",
        "2020-06-15T12:00:00+23:59"
    },
    My_data.
