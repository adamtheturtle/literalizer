-module(fixture_populated_and_empty_maps_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        #{}
    ],
    My_data.
