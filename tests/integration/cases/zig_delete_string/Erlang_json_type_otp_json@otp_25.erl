-module(fixture_zig_delete_string_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"v"/utf8>> => <<"ab"/utf8>>,
        <<"ab"/utf8>> => 1
    },
    My_data.
