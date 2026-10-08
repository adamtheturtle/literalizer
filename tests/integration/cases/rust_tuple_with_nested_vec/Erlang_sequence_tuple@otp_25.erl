-module(fixture_rust_tuple_with_nested_vec_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => {2, {}},
        "test" => {5, {"compile"}},
        "package" => {7, {"link", "test"}}
    },
    My_data.
