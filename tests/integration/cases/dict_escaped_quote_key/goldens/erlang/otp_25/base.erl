-module(fixture_dict_escaped_quote_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a\"b" => 1
    },
    My_data.
