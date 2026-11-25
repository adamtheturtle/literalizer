-module(fixture_dict_with_nulls_erlang_json_type_otp_json_nulls).
-export([x/0]).
x() ->
    My_data = #{
        <<"name"/utf8>> => <<"Alice"/utf8>>,
        <<"score"/utf8>> => null,
        <<"age"/utf8>> => 30
    },
    My_data.
