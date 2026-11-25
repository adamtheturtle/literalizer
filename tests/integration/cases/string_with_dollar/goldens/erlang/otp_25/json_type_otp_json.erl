-module(fixture_string_with_dollar_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"price $10"/utf8>>,
        <<"$HOME"/utf8>>
    ],
    My_data.
