-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "lint" => [2, [1]],
        "test" => [5, [7]]
    },
    My_data.
