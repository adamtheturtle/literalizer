-module(fixture_string_nul_before_hex_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"x"/utf8>> => <<"before\x{0}after"/utf8>>
    },
    My_data.
