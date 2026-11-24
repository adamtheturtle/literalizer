-module(fixture_scalar_int_negative_large_erlang_json_type_otp_json_negative_large).
-export([x/0]).
x() ->
    My_data = -2147483649,
    My_data.
