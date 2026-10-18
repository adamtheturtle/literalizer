-module(fixture_empty_map_nested_epoch_value_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"nested" => #{"times" => [{{1900, 1, 1}, {0, 0, 0}}]}},
        #{}
    ],
    My_data.
