-module(fixture_epoch_scalar_above_i32_range_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = <<"2099-06-15T08:30:00"/utf8>>,
    My_data.
