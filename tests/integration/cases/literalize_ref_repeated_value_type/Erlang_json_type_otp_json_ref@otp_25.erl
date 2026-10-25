-module(fixture_literalize_ref_repeated_value_type_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
    Shared = 42,
    My_data = [
        Shared,
        Shared
    ],
    My_data.
