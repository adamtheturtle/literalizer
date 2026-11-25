-module(fixture_epoch_datetime_map_values_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"within_i32"/utf8>> => <<"2024-01-15T12:00:00"/utf8>>,
        <<"beyond_i32"/utf8>> => <<"2099-06-15T08:30:00"/utf8>>
    },
    My_data.
