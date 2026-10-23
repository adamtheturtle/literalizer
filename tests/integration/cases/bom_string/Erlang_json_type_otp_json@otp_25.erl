-module(fixture_bom_string_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"x"/utf8>> => <<"﻿"/utf8>>
    },
    My_data.
