-module(fixture_call_existing_ref_arg_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Existing = 42,
    process(Existing).
