-module(fixture_comment_forbidden_characters_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,  % tab	here and bidi <U+202E>after
        "b" => 2
    },
    My_data.
