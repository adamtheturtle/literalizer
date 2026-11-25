-module(fixture_jsonc_comment_nulls_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % null heading
        % before null
        "a" => undefined,  % first null
        "b" => undefined  % second null
    },
    My_data.
