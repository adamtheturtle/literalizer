-module(fixture_tuple_nested_scope_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "x" => [1, [2, [3]]]
    },
    My_data.
