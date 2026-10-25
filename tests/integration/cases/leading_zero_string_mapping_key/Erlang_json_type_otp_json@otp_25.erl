-module(fixture_leading_zero_string_mapping_key_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"08"/utf8>> => <<"value"/utf8>>
    },
    My_data.
