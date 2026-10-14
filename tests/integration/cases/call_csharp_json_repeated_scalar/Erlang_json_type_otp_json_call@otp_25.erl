-module(fixture_call_csharp_json_repeated_scalar_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = 42,
    consume([Shared, Shared]).
