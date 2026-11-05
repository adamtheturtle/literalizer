-module(fixture_early_year_dates_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"date"/utf8>> => <<"0099-05-27"/utf8>>,
        <<"naive"/utf8>> => <<"0001-01-01T12:30:00"/utf8>>,
        <<"recent"/utf8>> => <<"2024-05-27T10:00:00"/utf8>>
    },
    My_data.
