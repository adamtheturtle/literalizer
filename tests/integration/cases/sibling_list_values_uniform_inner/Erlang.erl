-module(fixture_sibling_list_values_uniform_inner_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => [2, [1]],
        "test" => [5, [7]]
    },
    My_data.
