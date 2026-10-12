-module(fixture_v_empty_map_epoch_nested_value_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = [
        #{"nested" => #{"times" => [-2208988800]}},
        #{}
    ],
    My_data.
