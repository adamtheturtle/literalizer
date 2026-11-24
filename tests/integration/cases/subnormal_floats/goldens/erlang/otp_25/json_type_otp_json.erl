-module(fixture_subnormal_floats_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        5.0e-324,
        -5.0e-324,
        1.0e-310
    ],
    My_data.
