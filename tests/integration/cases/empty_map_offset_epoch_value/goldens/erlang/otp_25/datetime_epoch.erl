-module(fixture_empty_map_offset_epoch_value_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => 2208988800},
        #{}
    ],
    My_data.
