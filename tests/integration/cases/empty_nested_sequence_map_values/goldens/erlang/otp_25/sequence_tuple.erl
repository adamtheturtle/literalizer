-module(fixture_empty_nested_sequence_map_values_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "alpha" => {2, {}},
        "beta" => {5, {"x"}}
    },
    My_data.
