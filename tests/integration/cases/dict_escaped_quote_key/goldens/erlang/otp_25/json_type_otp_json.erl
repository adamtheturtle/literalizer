-module(fixture_dict_escaped_quote_key_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"a\"b"/utf8>> => 1
    },
    My_data.
