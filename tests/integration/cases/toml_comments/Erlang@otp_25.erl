-module(fixture_toml_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % before
        "answer" => 42,  % inline
        "plain" => "ok"
        % trailing
    },
    My_data.
