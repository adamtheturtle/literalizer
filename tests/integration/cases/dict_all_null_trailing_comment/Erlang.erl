-module(fixture_dict_all_null_trailing_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => undefined,
        "b" => undefined
        % trailing
    },
    My_data.
