-module(fixture_v_empty_map_epoch_offset_value_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => "2040-01-01T03:00:00+03:00"},
        #{}
    ],
    My_data.
