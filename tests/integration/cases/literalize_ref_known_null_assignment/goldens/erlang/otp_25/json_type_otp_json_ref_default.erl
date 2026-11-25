-module(fixture_literalize_ref_known_null_assignment_erlang_json_type_otp_json_ref_default).
-export([x/0]).
x() ->
    Item = null,
    My_data = Item,
    My_data.
