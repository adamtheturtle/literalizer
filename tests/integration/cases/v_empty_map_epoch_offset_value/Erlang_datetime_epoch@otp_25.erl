-module(fixture_v_empty_map_epoch_offset_value_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => 2208988800},
        #{}
    ],
    My_data.
