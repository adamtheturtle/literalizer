-module(fixture_no_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "message" => "no comment here"
    },
    My_data.
