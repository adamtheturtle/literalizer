-module(fixture_comment_trailing_backslash_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % comment ending backslash \ .
        "x" => 1
    },
    My_data.
