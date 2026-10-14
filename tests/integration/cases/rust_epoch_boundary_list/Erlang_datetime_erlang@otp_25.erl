-module(fixture_rust_epoch_boundary_list_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        {{1901, 12, 13}, {20, 45, 51}},
        {{1901, 12, 13}, {20, 45, 52}},
        {{2038, 1, 19}, {3, 14, 7}},
        {{2038, 1, 19}, {3, 14, 8}}
    ],
    My_data.
