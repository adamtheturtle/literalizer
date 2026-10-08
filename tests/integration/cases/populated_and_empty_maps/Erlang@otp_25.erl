-module(fixture_populated_and_empty_maps_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        #{}
    ],
    My_data.
