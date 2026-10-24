-module(fixture_bidi_formatting_string_with_nul_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"v"/utf8>> => <<"a‪\x{0}é😀b"/utf8>>
    },
    My_data.
