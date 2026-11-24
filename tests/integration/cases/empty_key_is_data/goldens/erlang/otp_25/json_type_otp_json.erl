-module(fixture_empty_key_is_data_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        #{<<""/utf8>> => <<"external_value"/utf8>>}
    ],
    My_data.
