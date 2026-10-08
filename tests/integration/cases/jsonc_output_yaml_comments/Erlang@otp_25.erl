-module(fixture_jsonc_output_yaml_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % server
        "host" => "localhost"  % default
    },
    My_data.
