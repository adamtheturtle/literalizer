-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "a" => undefined,
        "b" => undefined
        % trailing
    },
    My_data.
