-module(check).
-export([my_data/0]).
my_data() ->
    #{
    % Server configuration
    "host" => "localhost",  % default host
    "port" => 8080,
    % Enable debug mode
    "debug" => true
}.
