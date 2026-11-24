-module(fixture_inline_comment_trailing_backslash_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,  % inline ending backslash \ .
        "b" => 2
    },
    My_data.
