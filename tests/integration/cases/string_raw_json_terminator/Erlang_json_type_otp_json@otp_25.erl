-module(fixture_string_raw_json_terminator_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<")json"/utf8>> => <<"x"/utf8>>
    },
    My_data.
