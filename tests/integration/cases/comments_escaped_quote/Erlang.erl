-module(fixture_comments_escaped_quote_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "key" => "value \" # not a comment"  % real
    },
    My_data.
