-module(fixture_negative_epoch_datetime_list_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        "1960-01-01T00:00:00+00:00"
    },
    My_data.
