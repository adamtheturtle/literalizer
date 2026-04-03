-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"x" => 1},
        "b" => 2
    },
    My_data.
