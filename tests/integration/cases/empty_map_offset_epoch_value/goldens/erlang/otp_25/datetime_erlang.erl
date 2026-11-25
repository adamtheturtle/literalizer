-module(fixture_empty_map_offset_epoch_value_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => {{2040, 1, 1}, {3, 0, 0}}},
        #{}
    ],
    My_data.
