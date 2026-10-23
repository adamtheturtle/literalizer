-module(fixture_string_unicode_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"café"/utf8>>,
        <<"中文"/utf8>>,
        <<"😀"/utf8>>
    ],
    My_data.
