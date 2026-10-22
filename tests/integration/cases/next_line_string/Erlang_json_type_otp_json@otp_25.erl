-module(fixture_next_line_string_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"x"/utf8>> => <<"\x{85}"/utf8>>
    },
    My_data.
