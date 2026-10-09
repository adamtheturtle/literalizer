-module(fixture_mojo_empty_map_epoch_sibling_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => 1577836800},
        #{}
    ],
    My_data.
