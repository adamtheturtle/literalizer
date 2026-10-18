-module(fixture_epoch_boundary_set_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        {{1901, 12, 13}, {20, 45, 51}},
        {{1901, 12, 13}, {20, 45, 52}},
        {{2038, 1, 19}, {3, 14, 7}},
        {{2038, 1, 19}, {3, 14, 8}}
    ]),
    My_data.
