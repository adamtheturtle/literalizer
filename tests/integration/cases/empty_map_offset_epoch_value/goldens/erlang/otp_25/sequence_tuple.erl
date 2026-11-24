-module(fixture_empty_map_offset_epoch_value_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"timestamp" => "2040-01-01T03:00:00+03:00"},
        #{}
    },
    My_data.
