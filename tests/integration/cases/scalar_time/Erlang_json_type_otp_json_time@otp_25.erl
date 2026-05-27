-module(fixture_scalar_time_erlang_json_type_otp_json_time).
-export([x/0]).
x() ->
    My_data = #{
        <<"starts_at"/utf8>> => <<"09:30:00"/utf8>>
    },
    My_data.
