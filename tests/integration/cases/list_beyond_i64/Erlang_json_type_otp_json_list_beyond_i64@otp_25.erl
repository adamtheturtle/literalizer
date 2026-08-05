-module(fixture_list_beyond_i64_erlang_json_type_otp_json_list_beyond_i64).
-export([x/0]).
x() ->
    My_data = [
        9223372036854775807,
        9223372036854775808
    ],
    My_data.
