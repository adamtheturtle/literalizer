-module(fixture_v_empty_map_epoch_nested_value_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"nested" => #{"times" => ["1900-01-01T00:00:00+00:00"]}},
        #{}
    ],
    My_data.
