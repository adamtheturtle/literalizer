-module(fixture_dict_escaped_quote_key_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a\"b" => 1
    },
    My_data.
