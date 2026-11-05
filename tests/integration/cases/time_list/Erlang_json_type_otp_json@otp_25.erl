-module(fixture_time_list_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"times"/utf8>> => [<<"09:30:00"/utf8>>, <<"17:45:00"/utf8>>, <<"23:59:59"/utf8>>]
    },
    My_data.
