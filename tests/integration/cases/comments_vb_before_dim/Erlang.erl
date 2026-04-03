-module(check).
-export([x/0]).
x() ->
    My_data = #{
        % Configuration
        "name" => "app",
        % Port setting
        "port" => 3000
    },
    My_data.
