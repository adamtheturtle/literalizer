-module(fixture_sml_negative_epoch_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        {{1960, 1, 1}, {0, 0, 0}}
    ],
    My_data.
