-module(fixture_native_records_in_heterogeneous_sequences_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "h" => [1, "a", [2, "b"], #{"k" => [true]}]
    },
    My_data.
