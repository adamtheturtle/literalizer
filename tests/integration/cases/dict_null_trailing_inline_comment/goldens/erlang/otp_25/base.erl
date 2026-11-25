-module(fixture_dict_null_trailing_inline_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "host" => "localhost",
        "port" => undefined  % not configured yet
    },
    My_data.
