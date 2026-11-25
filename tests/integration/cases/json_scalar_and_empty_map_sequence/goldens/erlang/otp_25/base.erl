-module(fixture_json_scalar_and_empty_map_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        #{}
    ],
    My_data.
