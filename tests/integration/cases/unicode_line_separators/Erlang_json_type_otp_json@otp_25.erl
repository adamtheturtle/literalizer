-module(fixture_unicode_line_separators_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = <<"a\x{85}b\x{2028}c\x{2029}d\r\x{2028}e"/utf8>>,
    My_data.
