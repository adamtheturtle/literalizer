-module(fixture_dict_null_middle_inline_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "host" => "localhost",
        "port" => undefined,  % not configured yet
        "debug" => true
    },
    My_data.
