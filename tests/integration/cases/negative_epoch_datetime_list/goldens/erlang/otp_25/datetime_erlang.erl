-module(fixture_negative_epoch_datetime_list_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        {{1960, 1, 1}, {0, 0, 0}}
    ],
    My_data.
