-module(fixture_tuple_fields_with_nested_vectors_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => {2, {}},
        "test" => {5, {"compile"}},
        "package" => {7, {"link", "test"}}
    },
    My_data.
