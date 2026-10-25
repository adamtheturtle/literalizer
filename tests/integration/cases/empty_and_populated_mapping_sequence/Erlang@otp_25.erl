-module(fixture_empty_and_populated_mapping_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{},
        #{"value" => 1}
    ],
    My_data.
