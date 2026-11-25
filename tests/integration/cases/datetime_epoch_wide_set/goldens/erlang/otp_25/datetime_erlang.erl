-module(fixture_datetime_epoch_wide_set_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        {{2099, 6, 15}, {8, 30, 0}}
    ]),
    My_data.
