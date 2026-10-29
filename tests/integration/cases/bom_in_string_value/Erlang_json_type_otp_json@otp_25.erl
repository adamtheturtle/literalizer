-module(fixture_bom_in_string_value_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"v"/utf8>> => <<"a﻿b"/utf8>>
    },
    My_data.
