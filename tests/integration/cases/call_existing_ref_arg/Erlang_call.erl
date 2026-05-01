-module(fixture_call_existing_ref_arg_erlang_call).
-export([x/0]).
send(_) -> ok.
x() ->
    Existing = 42,
    send(Existing).
