-module(fixture_closing_bracket_string_boundaries_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"]"/utf8>>,
        <<"a]"/utf8>>,
        <<"a]="/utf8>>,
        <<"a]b"/utf8>>
    ],
    My_data.
