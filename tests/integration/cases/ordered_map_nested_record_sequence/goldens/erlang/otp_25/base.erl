-module(fixture_ordered_map_nested_record_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"entries", [#{"id" => 1}]}
    ],
    My_data.
