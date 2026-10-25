-module(fixture_scalar_empty_and_populated_maps_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        #{},
        #{"x" => 2}
    ],
    My_data.
