-module(fixture_delete_character_in_key_and_value_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"v"/utf8>> => <<"ab"/utf8>>,
        <<"ab"/utf8>> => 1
    },
    My_data.
