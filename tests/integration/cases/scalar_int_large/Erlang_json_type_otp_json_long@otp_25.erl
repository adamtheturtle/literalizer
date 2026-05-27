-module(fixture_scalar_int_large_erlang_json_type_otp_json_long).
-export([x/0]).
x() ->
    My_data = 2147483648,
    My_data.
