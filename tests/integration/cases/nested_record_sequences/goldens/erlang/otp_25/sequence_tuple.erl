-module(fixture_nested_record_sequences_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {#{"a" => 1}},
        {#{"a" => 2}}
    },
    My_data.
