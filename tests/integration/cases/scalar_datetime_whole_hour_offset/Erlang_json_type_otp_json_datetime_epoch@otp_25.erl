-module(fixture_scalar_datetime_whole_hour_offset_erlang_json_type_otp_json_datetime_epoch).
-export([x/0]).
x() ->
    My_data = <<"2024-01-15T18:00:00+05:00"/utf8>>,
    My_data.
