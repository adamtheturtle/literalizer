-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => [2, []],
        "test" => [5, ["compile"]]
    },
    My_data.
