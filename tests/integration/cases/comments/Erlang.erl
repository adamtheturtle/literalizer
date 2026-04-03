-module(check).
-export([x/0]).
x() ->
    My_data = #{
        % Server configuration
        "host" => "localhost",  % default host
        "port" => 8080,
        % Enable debug mode
        "debug" => true
    },
    My_data.
