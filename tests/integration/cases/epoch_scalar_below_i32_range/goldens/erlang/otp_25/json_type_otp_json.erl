-module(fixture_epoch_scalar_below_i32_range_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = <<"1901-12-13T20:45:51"/utf8>>,
    My_data.
