-module(fixture_binary_erlang_json_type_otp_json_binary).
-export([x/0]).
x() ->
    My_data = [
        <<"SGVsbG8="/utf8>>
    ],
    My_data.
