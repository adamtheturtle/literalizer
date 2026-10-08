-module(fixture_typed_sibling_maps_same_value_type_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"s" => 1},
        #{"t" => 3}
    ],
    My_data.
