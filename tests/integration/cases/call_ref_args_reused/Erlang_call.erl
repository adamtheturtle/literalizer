-module(fixture_call_ref_args_reused_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    Shared = 1,
    Other = 2,
    process(Shared, 1),
    process(Other, 0),
    process(Shared, 8).
