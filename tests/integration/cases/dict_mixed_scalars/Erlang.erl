-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => "x"
    },
    My_data.
