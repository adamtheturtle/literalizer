-module(fixture_toml_negative_integer_zero_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"value"/utf8>> => -0.0
    },
    My_data.
