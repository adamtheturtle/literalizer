-module(fixture_string_with_percent_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"100% done"/utf8>>,
        <<"%(name) is here"/utf8>>
    ],
    My_data.
