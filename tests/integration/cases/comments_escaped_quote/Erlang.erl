-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "key" => "value \" # not a comment"  % real
    },
    My_data.
