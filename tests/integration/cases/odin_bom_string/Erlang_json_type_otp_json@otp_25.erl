-module(fixture_odin_bom_string_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"v"/utf8>> => <<"a﻿b"/utf8>>
    },
    My_data.
