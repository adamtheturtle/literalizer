-module(fixture_call_json_repeated_array_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = [
        1,
        2
    ],
    consume([Shared, Shared]).
