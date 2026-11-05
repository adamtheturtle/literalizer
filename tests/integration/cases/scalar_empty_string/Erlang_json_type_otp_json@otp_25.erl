-module(fixture_scalar_empty_string_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = <<""/utf8>>,
    My_data.
