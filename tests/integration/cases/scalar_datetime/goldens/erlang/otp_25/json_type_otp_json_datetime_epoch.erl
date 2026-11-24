-module(fixture_scalar_datetime_erlang_json_type_otp_json_datetime_epoch).
-export([x/0]).
x() ->
    My_data = <<"2024-01-15T12:30:00+00:00"/utf8>>,
    My_data.
