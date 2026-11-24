-module(fixture_comments_escaped_single_quote_multiple_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "host" => "it's here",  % a comment
        "port" => 80  % another
    },
    My_data.
