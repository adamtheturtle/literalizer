-module(fixture_call_ref_null_consumable_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    My_null = null,
    Regular_null = null,
    consume(My_null),
    consume(Regular_null).
