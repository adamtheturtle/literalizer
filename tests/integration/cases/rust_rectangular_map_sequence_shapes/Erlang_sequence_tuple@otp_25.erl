-module(fixture_rust_rectangular_map_sequence_shapes_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => {#{"item" => {1}}},
        "b" => {#{"item" => {2}}}
    },
    My_data.
