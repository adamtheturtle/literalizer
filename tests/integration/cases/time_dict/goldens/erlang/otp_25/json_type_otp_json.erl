-module(fixture_time_dict_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"morning"/utf8>> => <<"09:30:00"/utf8>>,
        <<"afternoon"/utf8>> => <<"14:15:00"/utf8>>,
        <<"evening"/utf8>> => <<"23:59:59"/utf8>>
    },
    My_data.
