-module(fixture_literalize_ref_value_type_root_null_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
    Shared = null,
    My_data = Shared,
    My_data.
