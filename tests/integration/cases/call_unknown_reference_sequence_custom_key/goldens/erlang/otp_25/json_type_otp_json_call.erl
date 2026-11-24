-module(fixture_call_unknown_reference_sequence_custom_key_erlang_json_type_otp_json_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Untyped_value = [],
    process([Untyped_value, Untyped_value]).
