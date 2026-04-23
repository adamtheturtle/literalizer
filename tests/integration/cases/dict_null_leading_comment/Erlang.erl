-module(check).
-export([x/0]).
x() ->
    My_data = #{
        % comment
        "name" => "Alice",
        "score" => undefined
    },
    My_data.
