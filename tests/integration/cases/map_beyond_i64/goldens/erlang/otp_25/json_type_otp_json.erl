-module(fixture_map_beyond_i64_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"a"/utf8>> => 9223372036854775807,
        <<"b"/utf8>> => 9223372036854775808
    },
    My_data.
