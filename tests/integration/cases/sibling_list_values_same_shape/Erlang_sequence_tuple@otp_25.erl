-module(fixture_sibling_list_values_same_shape_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "test" => {5, {"compile"}},
        "package" => {7, {"link", "test"}}
    },
    My_data.
