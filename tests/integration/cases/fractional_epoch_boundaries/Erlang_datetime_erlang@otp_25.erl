-module(fixture_fractional_epoch_boundaries_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        {{1970, 1, 1}, {0, 0, 0}},
        {{1969, 12, 31}, {23, 59, 59}},
        {{1970, 1, 1}, {0, 0, 1}}
    ],
    My_data.
