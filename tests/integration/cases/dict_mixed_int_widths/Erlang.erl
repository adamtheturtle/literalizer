-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => 3000000000,
        "c" => "x"
    },
    My_data.
