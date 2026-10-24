-module(fixture_sml_negative_epoch_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"1960-01-01T00:00:00+00:00"/utf8>>
    ],
    My_data.
