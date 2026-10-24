-module(fixture_native_records_in_heterogeneous_sequences_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "h" => {1, "a", {2, "b"}, #{"k" => {true}}}
    },
    My_data.
