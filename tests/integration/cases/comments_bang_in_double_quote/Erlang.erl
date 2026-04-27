-module(fixture_comments_bang_in_double_quote_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "key" => "\"bang!\""  % real
    },
    My_data.
