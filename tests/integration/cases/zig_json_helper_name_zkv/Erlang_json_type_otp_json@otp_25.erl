-module(fixture_zig_json_helper_name_zkv_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    ZKV = #{
        <<"a"/utf8>> => 1
    },
    ZKV.
