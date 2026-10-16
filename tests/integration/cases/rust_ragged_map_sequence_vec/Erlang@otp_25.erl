-module(fixture_rust_ragged_map_sequence_vec_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [#{"item" => [1]}],
        "b" => [#{"item" => [2, 3]}]
    },
    My_data.
