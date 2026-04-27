-module(fixture_sibling_list_values_nested_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => [2, []],
        "test" => [5, ["compile"]]
    },
    My_data.
