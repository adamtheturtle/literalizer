-module(fixture_literalize_ref_value_type_root_string_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
    Shared = <<"value"/utf8>>,
    My_data = Shared,
    My_data.
