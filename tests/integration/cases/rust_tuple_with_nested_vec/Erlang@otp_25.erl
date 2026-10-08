-module(fixture_rust_tuple_with_nested_vec_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => [2, []],
        "test" => [5, ["compile"]],
        "package" => [7, ["link", "test"]]
    },
    My_data.
