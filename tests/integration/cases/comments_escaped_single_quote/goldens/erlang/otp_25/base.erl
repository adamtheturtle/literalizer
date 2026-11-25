-module(fixture_comments_escaped_single_quote_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "key" => "it's here"  % a comment
    },
    My_data.
