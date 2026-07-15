-module(fixture_json_string_escaping_erlang_json_type_otp_json_string_escaping).
-export([x/0]).
x() ->
    My_data = <<"a\"b\tcé"/utf8>>,
    My_data.
