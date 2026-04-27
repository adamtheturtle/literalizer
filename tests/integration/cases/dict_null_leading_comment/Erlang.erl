-module(fixture_dict_null_leading_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % comment
        "name" => "Alice",
        "score" => undefined
    },
    My_data.
