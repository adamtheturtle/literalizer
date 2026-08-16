-module(fixture_erlang_noncharacter_string_erlang_otp_json_noncharacter_string).
-export([x/0]).
x() ->
    My_data = #{
        <<"fffe"/utf8>> => <<65534/utf8>>,
        <<"ffff"/utf8>> => <<65535/utf8>>
    },
    My_data.
