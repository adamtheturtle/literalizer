-module(fixture_ragged_map_sequence_values_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => {#{"item" => {1}}},
        "b" => {#{"item" => {2, 3}}}
    },
    My_data.
