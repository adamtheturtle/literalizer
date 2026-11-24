-module(fixture_record_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"id" => 1, "label" => "first", "tags" => []},
        #{"id" => 2, "label" => "second", "tags" => []},
        #{"id" => 3, "label" => "third", "tags" => []}
    ],
    My_data.
