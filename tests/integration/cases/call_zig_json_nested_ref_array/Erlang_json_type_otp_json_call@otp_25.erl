-module(fixture_call_zig_json_nested_ref_array_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = [
        1,
        2
    ],
    consume([Shared, 42]).
