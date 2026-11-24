-module(fixture_literalize_ref_forced_camel_name_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
    UserObj = #{
        <<"_"/utf8>> => <<"_"/utf8>>
    },
    My_data = UserObj,
    My_data.
