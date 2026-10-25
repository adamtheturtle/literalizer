-module(fixture_scalar_and_populated_map_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        #{"a" => 2}
    ],
    My_data.
