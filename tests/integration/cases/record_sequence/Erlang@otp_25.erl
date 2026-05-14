-module(fixture_record_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"id" => 1, "label" => "first"},
        #{"id" => 2, "label" => "second"},
        #{"id" => 3, "label" => "third"}
    ],
    My_data.
