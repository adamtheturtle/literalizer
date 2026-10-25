-module(fixture_zig_json_helper_name_zval_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    ZVal = #{
        <<"a"/utf8>> => 1
    },
    ZVal.
