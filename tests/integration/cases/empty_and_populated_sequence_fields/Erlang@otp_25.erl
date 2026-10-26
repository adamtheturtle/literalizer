-module(fixture_empty_and_populated_sequence_fields_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"value" => []},
        #{"value" => [1]}
    ],
    My_data.
