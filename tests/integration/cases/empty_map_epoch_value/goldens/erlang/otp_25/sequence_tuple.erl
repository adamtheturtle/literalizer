-module(fixture_empty_map_epoch_value_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"timestamp" => "2020-01-01T00:00:00+00:00"},
        #{}
    },
    My_data.
