-module(fixture_datetime_epoch_negative_set_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        -1
    ]),
    My_data.
