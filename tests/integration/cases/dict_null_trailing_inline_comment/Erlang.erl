-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "host" => "localhost",
        "port" => undefined  % not configured yet
    },
    My_data.
