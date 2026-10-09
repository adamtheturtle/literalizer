-module(fixture_mojo_empty_map_epoch_sibling_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => {{2020, 1, 1}, {0, 0, 0}}},
        #{}
    ],
    My_data.
