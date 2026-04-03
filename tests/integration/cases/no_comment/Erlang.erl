-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "message" => "no comment here"
    },
    My_data.
