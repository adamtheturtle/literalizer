-module(fixture_typed_sibling_maps_empty_values_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"m" => #{}},
        #{"m" => #{}}
    ],
    My_data.
