-module(fixture_datetime_epoch_negative_set_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        {{1969, 12, 31}, {23, 59, 59}}
    ]),
    My_data.
