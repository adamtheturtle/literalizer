-module(fixture_float_special_values_erlang_json_type_otp_json_float_specials).
-export([x/0]).
x() ->
    My_data = [
        inf,
        '-inf',
        nan
    ],
    My_data.
