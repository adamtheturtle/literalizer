-module(fixture_empty_map_nested_epoch_value_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"nested" => #{"times" => {"1900-01-01T00:00:00+00:00"}}},
        #{}
    },
    My_data.
